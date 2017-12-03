@ECHO OFF 
REM This file runs MAIN SCRIPT for ECG annually estimation
REM Define your paths here
REM Modify those lines with input and output directories

set VAR_PATH="C:\Users\HS_MichalP\Documents\Mike_priv\ECG_estimation_repo\EKG_estimation\logs"

REM Those are presetted values
python main.py  %VAR_PATH%
ECHO Main script executed
PAUSE