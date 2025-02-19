#!/bin/bash

SDK_DIR="$HOME/Downloads/.android_sdk"
SDK_ZIP_PATTERN="commandlinetools-linux-*_latest.zip"
SDK_ZIP_PATH=""

echo "Please download the Android SDK command line tools from the following URL:"
echo "(Scroll down to 'Command line tools only' section and download commandlinetools-linux_xxxxxxxx_latest.zip.)"
echo "https://developer.android.com/studio#downloads"
echo "Once downloaded, place the ZIP file in your Downloads directory."

read -p "Press Enter after you have downloaded the file into your Downloads folder..."

echo "Searching for the downloaded SDK file..."

SDK_ZIP_PATH=$(find $HOME/Downloads -type f -name "$SDK_ZIP_PATTERN" | head -n 1)

if [ -z "$SDK_ZIP_PATH" ]; then
  echo "No SDK zip file found that matches the pattern '$SDK_ZIP_PATTERN'. Please check your download."
  exit 1
fi

echo "Found SDK zip file: $SDK_ZIP_PATH"

echo "Creating .android_sdk directory and unzipping SDK..."
mkdir -p $SDK_DIR

unzip "$SDK_ZIP_PATH" -d $SDK_DIR/

echo "Updating ~/.zshrc with Android SDK paths..."
{
  echo 'export ANDROID_SDK_ROOT="$HOME/Downloads/.android_sdk"'
  echo 'export PATH="$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$PATH"'
  echo 'export PATH="$ANDROID_SDK_ROOT/emulator:$PATH"'
  echo 'export PATH="$ANDROID_SDK_ROOT/platform-tools:$PATH"'
} >> ~/.zshrc

echo "Applying changes to ~/.zshrc..."
zsh -i -c 'source ~/.zshrc'

echo "Installing Android SDK command line tools..."
yes | $ANDROID_SDK_ROOT/cmdline-tools/bin/sdkmanager --sdk_root=$ANDROID_SDK_ROOT "cmdline-tools;latest"

echo "Installing essential SDK packages and build tools..."
yes | sdkmanager "platforms;android-29" "build-tools;29.0.2"
yes | sdkmanager "extras;google;m2repository" "extras;android;m2repository"
yes | sdkmanager "platform-tools" "tools"
yes | sdkmanager --licenses

echo "Listing installed SDK packages..."
sdkmanager --list_installed

echo "Listing available system images..."
sdkmanager --list | grep system-images

echo "Installing system image..."
sdkmanager "system-images;android-29;google_apis_playstore;x86_64"

# Step 11: Create an Android Virtual Device (AVD)
echo "Creating Android Virtual Device (AVD)..."
avdmanager create avd -n device --device pixel -k "system-images;android-29;google_apis_playstore;x86_64"

# Step 12: List all AVDs
echo "Listing all AVDs..."
$ANDROID_SDK_ROOT/cmdline-tools/bin/avdmanager list avd

# Step 13: Start the AVD emulator
echo "Starting the AVD emulator..."
$ANDROID_SDK_ROOT/emulator/emulator -avd device
