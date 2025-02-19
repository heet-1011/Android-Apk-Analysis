#!/bin/bash

print_color() {
    echo -e "\033[32m$1\033[0m"
}
print_yellow() {
    echo -e "\033[93m$1\033[0m"
}
print_blue() {
    echo -e "\033[94m$1\033[0m"
}
print_rest() {
    bg_color=$(tput setab 0; tput colors)
    if [ "$bg_color" -le 8 ]; then
        text_color=15
    else
        text_color=0
    fi
    echo -e "\033[38;5;${text_color}m$1\033[0m"
}


echo -e "\033[1;34m"
print_color "======================================================="
print_color "                     rootAVD                          "
print_color "======================================================="
print_color "   Welcome to the AVD Rooting Automation Script! 🌟"
print_color "======================================================="
print_color "   This script will root your Android Virtual Device (AVD) "
print_color "   and ensure it gets proper permissions with Magisk. 🚀"
print_color "======================================================="

sleep 5

echo "Initializing the script..."
sleep 2
avd_status=$(adb devices | grep -w "device")
if [[ -z "$avd_status" ]]; then
    echo "AVD is not running, starting AVD..."
    emulator @device &> /dev/null &
    print_yellow "----------------------------------------------------------------------------------------"
    print_blue "Press Enter to continue once AVD has started and home screen is visible."
    print_yellow "----------------------------------------------------------------------------------------"
    read -r user_input
else
    echo "AVD is already running."
fi

echo "Cloning rootAVD repository..."
git clone https://github.com/heet-1011/rootAVD-forked.git
cd rootAVD-forked || exit

echo "Rooting the AVD..."
chmod +x rootAVD.sh
./rootAVD.sh system-images/android-29/google_apis_playstore/x86_64/ramdisk.img

print_yellow "----------------------------------------------------------------------------------------"
print_blue "Waiting for AVD to shutdown. You can manually shutdown if not done automatically."
print_blue "Press Enter to continue once it has shut down."
print_yellow "----------------------------------------------------------------------------------------"
read -r user_input

echo "Restarting the AVD..."
emulator @device &> /dev/null &
print_yellow "----------------------------------------------------------------------------------------"
print_blue "Press Enter to continue once it has restarted and home screen is visible."
print_yellow "----------------------------------------------------------------------------------------"
read -r user_input

echo "Opening Magisk app..."
adb shell am start -n com.topjohnwu.magisk/com.topjohnwu.magisk.ui.MainActivity
print_yellow "----------------------------------------------------------------------------------------"
print_blue "AVD : Press Ok in 'Request Addition setup' popup in Magisk app."
print_blue "Press Enter to continue once it has restarted and home screen is visible."
print_yellow "----------------------------------------------------------------------------------------"
read -r user_input

echo "Opening Magisk app and granting root permission..."
adb shell am start -n com.topjohnwu.magisk/com.topjohnwu.magisk.ui.MainActivity
print_yellow "----------------------------------------------------------------------------------------"
print_blue "Press Enter to continue once Magisk app is started."
print_yellow "----------------------------------------------------------------------------------------"
read -r user_input

echo "Granting root permission in terminal..."
print_yellow "----------------------------------------------------------------------------------------"
print_blue "AVD : Press Grant button in pop up in Magisk app."
print_blue "Waiting for the Magisk request to pop up for granting root access..."
adb shell "su -c 'sleep 5; exit; sleep 5; exit'"
print_blue "Press Enter to continue once done with pressing grant button."
print_yellow "----------------------------------------------------------------------------------------"
read -r user_input

echo "Verifying root access..."
root_user=$(adb shell "su -c 'whoami'")
echo "Root user: $root_user"
if [[ "$root_user" == "root" ]]; then
    echo "AVD successfully rooted!"
else
    echo "Error rooting the device."
fi

echo "Closing Magisk app..."
adb shell am force-stop com.topjohnwu.magisk
sleep 2

echo "Shutting down the AVD..."
adb emu kill
sleep 2
echo "AVD has been successfully shut down."
