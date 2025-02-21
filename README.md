# Android-Apk-Analysis

## Prerequisite Setup
- [Setup Guide](https://github.com/heet-1011/Android-Apk-Analysis/blob/main/prerequisite-setup/README.md)
- `sudo apt install apktool`
- `sudo apt install dex2jar`
- `sudo apt install jd-gui`
  
## Static Analysis
- Decompile APK : `apktool d report.apk -o decompiled_app`
<br> or 
- Decompile APK without decompiling src code
  * Decompile APK : `apktool d -s report.apk -o decompiled_app_with_dex`
  * Convert dex files to jar : `d2j-dex2jar classes.dex`
  * View java src code : `jd-gui classes-dex2jar.jar`
- Generate Key : `keytool -genkey -v -keystore my-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias my-key`
- Recompile APK : `apktool b <decompiled_directory>`
- Zip align (to ensures that all uncompressed data sections in the APK file are aligned on 4-byte boundaries, improving performance when the APK is installed on devices) : `zipalign -p -f 4 aligned-sample.apk <decompiled_directory>/dist/*.apk`
- Sign APK : `apksigner sign --ks my-release-key.jks --out signed-sample.apk aligned-sample.apk`

## Dynamic Analysis
- Open terminal and move to Downloads directory `cd $HOME/Downloads`
- Clone src code directory `git clone https://github.com/heet-1011/Android-Apk-Analysis.git`
- Move to directory `cd Android-Apk-Analysis/src` 
- Create python venv `python -m venv analysis`
- Start venv `source analysis/bin/activate`
- Install required libraries `pip install -r requirements.txt`
- Execute script `python dynamic_analysis.py`
- Once script is executed successfully, all generated logs will be stored at `$HOME/Downloads/dynamic-analysis` directory.
