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
- `--model` (default: longterm_avg): Model type
- `--refit` (default: True): Re-fit model from scratch
- `--validate` (default: True): Run validation and show plots

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
- `--model` (default: longterm_avg): Model type

### `forecast_functions.py`
Contains shared utility functions used by both training and forecasting scripts:
- `get_training_test_data()`: Downloads and splits streamflow data
- `get_recent_data()`: Retrieves recent observations for forecasting
- `fit_longterm_avg_model()`: Fits the long-term average model
- `make_5day_forecast_longterm()`: Generates 5-day predictions
- `compute_metrics()`: Calculates validation metrics (NSE, RMSE, etc.)
- `plot_validation()`: Visualizes model performance
- `save_model()` / `load_model()`: Model persistence

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

| Parameter | Default | Description |
|-----------|---------|-------------|
| gauge-id | 09506000 | USGS gauge for Verde River near Camp Verde, AZ |
| ar-order | 7 | Autoregressive lag order (days) |
| train-start | 1990-01-01 | Training period start |
| train-end | 2022-12-31 | Training period end |
| test-start | 2023-01-01 | Test/validation period start |
| test-end | 2024-12-31 | Test/validation period end |
| forecast-date | 2024-04-30 | Start date for 5-day forecast |

## Model

**Long-term Average Model**: Predicts streamflow as the mean of all observations in the training period. Provides a baseline for comparison with more sophisticated approaches.

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
