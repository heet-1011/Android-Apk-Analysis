# Android-Apk-Analysis

## Prerequisite Setup
[Setup Guide](https://github.com/heet-1011/Android-Apk-Analysis/blob/main/prerequisite-setup/README.md)

## Dynamic Analysis
- Clone src code directory `git clone https://github.com/heet-1011/Android-Apk-Analysis.git`
- Move to directory `cd Android-Apk-Analysis/src` 
- Create python venv `python -m venv analysis`
- Start venv `source analysis/bin/activate`
- Install required libraries `pip install -r requirements.txt`
- Execute script `python dynamic_analysis.py`
- Once script is executed successfully, all generated logs will be stored at `$HOME/Downloads/dynamic-analysis` directory.
