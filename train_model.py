"""
train_model.py
--------------
Fits the chosen model on the training period and optionally validates on the
test period. Run via run_workflow.sh, or directly:

    python train_model.py --email YOU@EMAIL.COM --pin 1234 [--other-options]
"""

import os
import argparse
import pandas as pd
import hf_hydrodata
from forecast_functions import (
    get_training_test_data,
    fit_longterm_avg_model,
    compute_metrics,
    plot_validation,
    save_model,
    load_model,
)

parser = argparse.ArgumentParser()
parser.add_argument('--email',       required=True)
parser.add_argument('--pin',         required=True)
parser.add_argument('--gauge-id',    default='09506000')
parser.add_argument('--ar-order',    type=int, default=7)
parser.add_argument('--train-start', default='1990-01-01')
parser.add_argument('--train-end',   default='2022-12-31')
parser.add_argument('--test-start',  default='2023-01-01')
parser.add_argument('--test-end',    default='2024-12-31')
parser.add_argument('--model',       default='longterm_avg', choices=['longterm_avg', 'day_of_week'])
parser.add_argument('--refit',       default='True')
parser.add_argument('--validate',    default='True')
args = parser.parse_args()

REFIT_MODEL    = args.refit.lower()    == 'true'
RUN_VALIDATION = args.validate.lower() == 'true'

hf_hydrodata.register_api_pin(email=args.email, pin=args.pin)

print("\n--- Step 1: Download streamflow data ---")
train, test = get_training_test_data(
    args.gauge_id, args.train_start, args.train_end,
    args.test_start, args.test_end
)

# ── Long-term average model ───────────────────────────────────────────────────
if args.model == 'longterm_avg':
    print("\n--- Step 2: Fit long-term average model ---")
    if REFIT_MODEL or not os.path.exists('saved_model.pkl'):
        mean_flow = fit_longterm_avg_model(train)
        print(f"  Long-term mean: {mean_flow:.2f} cfs")
        save_model(mean_flow)
    else:
        mean_flow = load_model()
        if not isinstance(mean_flow, float):
            raise TypeError(
                "saved_model.pkl does not contain a longterm_avg model. "
                "Re-run with --refit True --model longterm_avg to train one."
            )

    if RUN_VALIDATION:
        print("\n--- Step 3: Validate on test period ---")
        train_fitted    = pd.Series(mean_flow, index=train.index)
        forecast_series = pd.Series(mean_flow, index=test.index)

        metrics = compute_metrics(test['streamflow_cfs'].values, forecast_series.values)
        print("\n  Validation metrics:")
        for name, val in metrics.items():
            print(f"    {name:<12}: {val:.4f}")
        print("\n  NSE guide: >0.75 very good | 0.65–0.75 good | "
              "0.50–0.65 satisfactory | <0.50 poor")

        print("\n  Generating validation plot ...")
        plot_validation(
            train['streamflow_cfs'], test['streamflow_cfs'],
            forecast_series, metrics, 'Long-term Average',
            train_forecast_cfs=train_fitted
        )

# ── Day of week model ─────────────────────────────────────────────────────────
if args.model == 'day_of_week':
    print("\n--- Step 2: Fit day-of-week model ---")
    # Assign flow values by day of week — Monday highest, Friday lowest
    # because rivers are most energetic at the start of the work week
    dow_flows = {
        0: 800.0,   # Monday    — rivers start the week strong
        1: 650.0,   # Tuesday   — still going
        2: 500.0,   # Wednesday — midweek slump
        3: 350.0,   # Thursday  — almost Friday
        4: 200.0,   # Friday    — rivers take it easy
        5: 450.0,   # Saturday  — weekend rebound
        6: 600.0,   # Sunday    — resting up for Monday
    }
    save_model(dow_flows)
    print("  Day-of-week flow assignments:")
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    for i, day in enumerate(days):
        print(f"    {day:<12}: {dow_flows[i]:.1f} cfs")

    if RUN_VALIDATION:
        print("\n--- Step 3: Validate day-of-week model on test period ---")
        forecast_series = pd.Series(
            [dow_flows[d.weekday()] for d in test.index],
            index=test.index
        )
        train_fitted = pd.Series(
            [dow_flows[d.weekday()] for d in train.index],
            index=train.index
        )
        metrics = compute_metrics(test['streamflow_cfs'].values, forecast_series.values)
        print("\n  Validation metrics:")
        for name, val in metrics.items():
            print(f"    {name:<12}: {val:.4f}")

        plot_validation(
            train['streamflow_cfs'], test['streamflow_cfs'],
            forecast_series, metrics, 'Day of Week',
            train_forecast_cfs=train_fitted
        )

print("\nTraining complete.")
