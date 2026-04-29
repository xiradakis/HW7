@echo off
REM run_workflow.bat
REM ----------------
REM DRIVER SCRIPT — set your options here and run:
REM
REM   run_workflow.bat

REM =============================================================================
REM USER OPTIONS — edit these before running
REM =============================================================================

set GAUGE_ID=09506000
set AR_ORDER=7

set TRAIN_START=1990-01-01
set TRAIN_END=2022-12-31
set TEST_START=2023-01-01
set TEST_END=2024-12-31

set FORECAST_DATE=2025-04-30
set REFIT_MODEL=True
set RUN_VALIDATION=True
set MODEL=longterm_avg

REM =============================================================================
REM RUN WORKFLOW — no need to edit below this line
REM =============================================================================

set /p EMAIL=HydroFrame email: 
set /p PIN=HydroFrame PIN: 

if "%REFIT_MODEL%"=="True" goto run_train
if "%RUN_VALIDATION%"=="True" goto run_train
goto run_forecast

:run_train
python train_model.py ^
    --email        %EMAIL%        ^
    --pin          %PIN%          ^
    --gauge-id     %GAUGE_ID%     ^
    --ar-order     %AR_ORDER%     ^
    --train-start  %TRAIN_START%  ^
    --train-end    %TRAIN_END%    ^
    --test-start   %TEST_START%   ^
    --test-end     %TEST_END%     ^
    --model        %MODEL%        ^
    --refit        %REFIT_MODEL%  ^
    --validate     %RUN_VALIDATION%

:run_forecast
python generate_forecast.py ^
    --email         %EMAIL%         ^
    --pin           %PIN%           ^
    --gauge-id      %GAUGE_ID%      ^
    --ar-order      %AR_ORDER%      ^
    --forecast-date %FORECAST_DATE% ^
    --model         %MODEL%

pause
