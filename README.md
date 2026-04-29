# HW7: Verde River Streamflow Forecasting

A machine learning-based streamflow forecasting system for the Verde River near Camp Verde, Arizona (USGS Gauge ID: 09506000). This project downloads historical USGS data, trains predictive models, and generates 5-day streamflow forecasts.

## Overview

This project implements a complete workflow for:
- **Data Collection**: Downloads daily streamflow data using the HydroFrame API
- **Model Training**: Fits a long-term average model on historical training data (1990–2022)
- **Validation**: Evaluates model performance on test data (2023–2024)
- **Forecasting**: Generates 5-day streamflow predictions for a specified start date

## Project Structure

```
├── train_model.py              # Model training and validation script
├── generate_forecast.py        # Forecast generation script
├── forecast_functions.py       # Shared helper functions
├── run_workflow.sh             # Bash driver script (Linux/macOS)
├── run_workflow.bat            # Batch driver script (Windows)
├── environment.yml             # Conda environment specification
└── README.md                   # This file
```

## Files

### `train_model.py`
Trains the long-term average model on historical streamflow data and validates performance on a test set.

**Usage:**
```bash
python train_model.py --email YOUR_EMAIL@example.com --pin YOUR_PIN [OPTIONS]
```

**Key Arguments:**
- `--email` (required): HydroFrame API email
- `--pin` (required): HydroFrame API PIN
- `--gauge-id` (default: 09506000): USGS gauge ID
- `--ar-order` (default: 7): Number of lag days
- `--train-start` (default: 1990-01-01): Training period start date
- `--train-end` (default: 2022-12-31): Training period end date
- `--test-start` (default: 2023-01-01): Test period start date
- `--test-end` (default: 2024-12-31): Test period end date
- `--model` (default: longterm_avg): Model type (`longterm_avg` or `day_of_week`)
- `--refit` (default: True): Re-fit model from scratch
- `--validate` (default: True): Run validation and show plots

**Example:**
```bash
# Train long-term average model
python train_model.py --email you@example.com --pin 1234 --model longterm_avg

# Train day-of-week model
python train_model.py --email you@example.com --pin 1234 --model day_of_week --validate True
```

### `generate_forecast.py`
Generates a 5-day streamflow forecast using the trained model.

**Usage:**
```bash
python generate_forecast.py --email YOUR_EMAIL@example.com --pin YOUR_PIN [OPTIONS]
```

**Key Arguments:**
- `--email` (required): HydroFrame API email
- `--pin` (required): HydroFrame API PIN
- `--gauge-id` (default: 09506000): USGS gauge ID
- `--ar-order` (default: 7): Number of lag days
- `--forecast-date` (default: 2024-04-30): Start date for 5-day forecast (YYYY-MM-DD)
- `--model` (default: longterm_avg): Model type (`longterm_avg` or `day_of_week`)

**Example:**
```bash
# Generate forecast with long-term average model
python generate_forecast.py --email you@example.com --pin 1234 --forecast-date 2024-05-01

# Generate forecast with day-of-week model
python generate_forecast.py --email you@example.com --pin 1234 --model day_of_week --forecast-date 2024-05-01
```

### `forecast_functions.py`
Contains shared utility functions used by both training and forecasting scripts:
- `get_training_test_data()`: Downloads and splits streamflow data
- `get_recent_data()`: Retrieves recent observations for forecasting
- `fit_longterm_avg_model()`: Fits the long-term average model (returns mean flow)
- `make_5day_forecast_longterm()`: Generates 5-day predictions using long-term mean
- `compute_metrics()`: Calculates validation metrics (NSE, RMSE, R², etc.)
- `plot_validation()`: Visualizes model performance on test set
- `save_model()` / `load_model()`: Model persistence (pickle-based)

### `run_workflow.sh` (Linux/macOS)
Complete driver script that prompts for HydroFrame credentials and runs the full workflow:
1. Trains the model
2. Generates forecast
3. Displays results

**Usage:**
```bash
bash run_workflow.sh
```

### `run_workflow.bat` (Windows)
Windows equivalent of the bash workflow script.

**Usage:**
```bash
run_workflow.bat
```

### `environment.yml`
Conda environment specification. Contains all required dependencies.

## Setup & Installation

### Prerequisites
- Python 3.8+
- Conda or Miniconda
- HydroFrame API credentials (email and PIN)
  - Register at: https://hydroframe.org

### Step 1: Create Conda Environment
```bash
conda env create -f environment.yml
conda activate verde-forecast
```

### Step 2: Run Workflow
```bash
# Linux/macOS
bash run_workflow.sh

# Windows
run_workflow.bat
```

Or run scripts individually:
```bash
python train_model.py --email your@email.com --pin YOUR_PIN
python generate_forecast.py --email your@email.com --pin YOUR_PIN --forecast-date 2024-05-01
```

## Key Parameters

| Parameter | Default | Description | Notes |
|-----------|---------|-------------|-------|
| gauge-id | 09506000 | USGS gauge for Verde River near Camp Verde, AZ | — |
| ar-order | 7 | Autoregressive lag order (days) | Used for recent data validation |
| train-start | 1990-01-01 | Training period start | Long-term avg model only |
| train-end | 2022-12-31 | Training period end | Long-term avg model only |
| test-start | 2023-01-01 | Test/validation period start | Validation only |
| test-end | 2024-12-31 | Test/validation period end | Validation only |
| forecast-date | 2024-04-30 | Start date for 5-day forecast | Must have recent observations available |
| model | longterm_avg | Model selection | `longterm_avg` or `day_of_week` |

## Models

This project implements two streamflow forecasting models:

### Long-term Average Model
Predicts streamflow as the **mean of all observations in the training period**. Provides a simple baseline for comparison.

**Characteristics:**
- Constant prediction for every day
- Mean streamflow typically ~1000–2000 cfs for Verde River
- Simple, interpretable, computationally efficient
- Provides baseline accuracy metric

**Use case:** Baseline reference; useful when recent observations are unavailable.

### Day-of-Week Model
Assigns different streamflow values based on the **day of the week**. Captures weekly patterns in river flows.

**Flow assignments:**
- **Monday**: 800 cfs (rivers start the week strong)
- **Tuesday**: 650 cfs (still flowing well)
- **Wednesday**: 500 cfs (midweek slump)
- **Thursday**: 350 cfs (almost Friday)
- **Friday**: 200 cfs (rivers take it easy)
- **Saturday**: 450 cfs (weekend rebound)
- **Sunday**: 600 cfs (resting up for Monday)

**Characteristics:**
- Cyclical pattern repeats weekly
- Captures human-influenced flow patterns
- Fast prediction based on calendar
- Does not use recent observations

**Use case:** Exploratory model; demonstrates weekly periodicity in streamflow data.

## Model Selection

Choose your model via the `--model` flag:

```bash
# Use long-term average (smooth, constant predictions)
python train_model.py --email you@example.com --pin 1234 --model longterm_avg
python generate_forecast.py --email you@example.com --pin 1234 --model longterm_avg

# Use day-of-week (weekly pattern predictions)
python train_model.py --email you@example.com --pin 1234 --model day_of_week
python generate_forecast.py --email you@example.com --pin 1234 --model day_of_week
```

### Model Comparison

| Feature | Long-term Average | Day-of-Week |
|---------|-------------------|-------------|
| **Prediction** | Constant mean flow | Varies by day of week |
| **Training required** | Yes (computes mean) | Minimal (uses fixed values) |
| **Validation** | Full test set evaluation | N/A |
| **Refit needed** | When training data changes | Not applicable |
| **Accuracy** | Baseline metric (usually poor) | Exploratory (captures cycles) |
| **Use case** | Reference forecast | Pattern detection |
| **Computational cost** | Minimal | Negligible |

## Output

- **Trained Model**: Saved to `saved_model.pkl` after training
- **Validation Plots**: Shows predictions vs. observations on test set
- **Forecast Table**: 5-day streamflow forecast with predicted values
- **Metrics**: NSE (Nash-Sutcliffe Efficiency), RMSE, MAE, etc.

## Dependencies

Key packages (see environment.yml for full list):
- `pandas`: Data manipulation
- `numpy`: Numerical computing
- `matplotlib`: Visualization
- `hf_hydrodata`: HydroFrame API client
- `scikit-learn`: Machine learning utilities (if applicable)

## Notes

- The Verde River gauge ID (09506000) is near Camp Verde, Arizona
- Training uses 1990–2022 data; validation uses 2023–2024 data
- Forecast dates must have sufficient recent observations available
- Log-transformation is applied to streamflow for modeling

## License

Homework assignment for Analysis Tools & Methods II at University of Arizona
