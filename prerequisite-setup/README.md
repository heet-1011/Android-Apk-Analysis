## Setup Guide
### Automatic setup guide
- Download [install_emulator.sh](https://github.com/heet-1011/Android-Apk-Analysis/blob/main/prerequisite-setup/install_emulator.sh)
- Give executable permission using `chmod +x install_emulator.sh`
- Execute : `./install_emulator.sh`
- Once AVD is successfully installed Download [root_emulator.sh](https://github.com/heet-1011/Android-Apk-Analysis/blob/main/prerequisite-setup/root_emulator.sh)
- Give executable permission using `chmod +x root_emulator.sh`
- Execute : `./root_emulator.sh` (Note : While executing this script, manual inputs are required at certain points. Please pay close attention to all lines in the console that are surrounded by '-----------------------------' lines, as these indicate areas where input is needed. Additionally, ensure that you monitor any pop-up windows in the AVD during this process.)
### Manual setup guide
- **Android Virtual Device (AVD) Installation**
  * Visit [Android SDK official site](https://developer.android.com/studio#downloads). Scroll down to <span style="color: red;">**'Command line tools only'**</span> and download commandlinetools-linux_xxxxxxxx_latest.zip in Downloads folder. 
  * Unzip to `.android_sdk` directory.
    + `mkdir .android_sdk`
    + `unzip commandlinetools-linux-xxxxxx_latest.zip -d .android_sdk/`
  * Add path to `~/.zshrc` file.
    + `sudo vim ~/.zshrc`
    + Press I for insert mode.
    + Paste following path in the file :
      + `export ANDROID_SDK_ROOT="$HOME/Downloads/.android_sdk"`
      + `export PATH="$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$PATH"`
      + `export PATH="$ANDROID_SDK_ROOT/emulator:$PATH"`
      + `export PATH="$ANDROID_SDK_ROOT/platform-tools:$PATH"`
    + Press ESC.
    + `:wq` to save and exit.
  * Apply changes.
    + `source ~/.zshrc`
  * Install android sdk command line tool
    + `$ANDROID_SDK_ROOT/cmdline-tools/bin/sdkmanager --sdk_root=$ANDROID_SDK_ROOT "cmdline-tools;latest"`
  * Download and Install essential SDK packages and build tools for system image
    + `sdkmanager "platforms;android-29" "build-tools;29.0.2"`
    + `sdkmanager "extras;google;m2repository" "extras;android;m2repository"`
    + `sdkmanager "platform-tools" "tools"` 
    + `sdkmanager --licenses`
  * To list available SDK packages and system images.
    + `sdkmanager --list_installed`
    + `sdkmanager --list | grep system-images`
  * Install system image.
    + `sdkmanager "system-images;android-29;google_apis_playstore;x86_64"`
  * Create Android Virtual Device(AVD).
    + `avdmanager create avd -n device --device pixel -k "system-images;android-29;google_apis_playstore;x86_64"`
  * List all AVDs.
    + `avdmanager list avd`
  * To start AVD.
    + `emulator @device`

- **Root AVD**
  * Download rootAVG repo
    + `git clone https://github.com/heet-1011/rootAVD-forked.git`
  * Precondition
    + AVD is running.
    + adb shell will connect to the running AVD.
  * Change directory
    + `cd rootAVD-forked`
  * List all AVDs
    + `./rootAVD.sh ListAllAVDs`
  * Copy and Execute command similar to `./rootAVD.sh system-images/android-29/google_apis_playstore/x86_64/ramdisk.img` from output of above command corresponding to the emulators system-image
  * Wait for 10-20 seconds for emulator to shutdown if not do it manually.
  * Restart emulator with `emulator @device`.
  * Open Magisk app in your emulator.
  * Allow reboot pop-up.
  * Open terminal and execute `adb shell`.
  * Execute `su`.
  * After executing `su`, Magisk app will show one pop-up menu for SuperUser request. Grant Root permission.
  * To verify whether phone is rooted or not, execute `whoami` in the same terminal, if it returns **root** then root AVD is successful. 
