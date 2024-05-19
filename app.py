import sys
import subprocess
import re
import time
from lxml import etree
from androguard.core.apk import APK
from loguru import logger


def install_app(apk_path):
    try:
        # Construct the ADB command to install the APK
        # "-r" flag replaces existing application if present
        adb_command = ["adb", "install", "-r", apk_path]

        # Execute the ADB command
        subprocess.run(adb_command, check=True)
        print("App installed successfully")
    except subprocess.CalledProcessError as e:
        print("An error occurred:", e)


def launch_app(package_name, main_activity):
    try:
        # Construct the ADB command to launch the app
        adb_command = ["adb", "shell", "am", "start",
                       "-n",
                       f"{package_name}/{main_activity}"]

        # Execute the ADB command
        subprocess.run(adb_command, check=True)
        print("App launched successfully")
    except subprocess.CalledProcessError as e:
        print("An error occurred:", e)


def dumpsys_activity_display():
    try:
        # Construct the ADB command to run dumpsys activity
        adb_command = ["adb", "shell", "dumpsys", "activity", "activities"]

        activity_name = None
        while activity_name is None:
            # Execute the ADB command and capture the output
            output = subprocess.check_output(adb_command, universal_newlines=True)
            match = re.search(r'mCurrentFocus=.+\{.+ .+ (.+)}', output)
            if match:
                activity_name = match.group(1)
            else:
                time.sleep(5)
                print("We haven't found yet the displayed activity")

        return activity_name

    except subprocess.CalledProcessError as e:
        print("An error occurred:", e)
        return ""


def extract_ui():
    directory = '/sdcard'

    # Use uiautomator to dump UI layout of the activity
    ui_command = ["adb", "shell", "uiautomator", "dump", f"{directory}/ui_layout.xml"]
    subprocess.run(ui_command, check=True)

    # Pull the XML file from the device
    pull_command = ["adb", "pull", f"{directory}/ui_layout.xml", "ui_layout.xml"]
    subprocess.run(pull_command, check=True)

    # Delete the file from the device
    delete_command = ["adb", "shell", "rm", f"{directory}/ui_layout.xml"]
    subprocess.run(delete_command, check=True)

    print(f"UI layout saved successfully")


def delete_shared_preferences(package_name):

    # Construct the ADB command to delete shared preferences
    adb_delete_command = ["adb", "shell", "pm", "clear", package_name]

    # Run the ADB delete command
    subprocess.run(adb_delete_command)


def uninstall_app(package_name):
    # Construct the ADB command to uninstall the app
    adb_command = ["adb", "uninstall", package_name]

    # Run the ADB command
    process = subprocess.Popen(adb_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    # Check if the uninstallation was successful
    if process.returncode == 0:
        print("App uninstalled successfully")
    else:
        print(f"Failed to uninstall app. Error: {error.decode('utf-8')}")


def adb_click_button(bounds):
    # Extract bounds values
    left, top, right, bottom = map(int, bounds.replace("][", ",").replace("[", "").replace("]", "").split(","))

    # Calculate the coordinates of the center of the button
    x = (left + right) // 2
    y = (top + bottom) // 2

    # Send tap event using ADB
    subprocess.run(['adb', 'shell', 'input', 'tap', str(x), str(y)])


def click_skip():
    tree = etree.parse('ui_layout.xml')
    elements = tree.xpath("//*[contains(@class, 'android.widget.Button') and contains(@text, 'SKIP')]")

    if len(elements) != 1:
        print("There is no SKIP button")
    else:
        bounds = elements[0].attrib.get('bounds')
        adb_click_button(bounds)
        print("SKIP button clicked")


def main():
    # Disable logs
    logger.remove()

    if len(sys.argv) != 2:
        print("Something wrong with the command line argument")
        sys.exit(1)

    apk_path = sys.argv[1]
    a = APK(apk_path)

    install_app(apk_path)

    package_name = a.get_package()
    main_activity = a.get_main_activity()
    launch_app(package_name, main_activity)
    time.sleep(5)

    displayed_activity_info = dumpsys_activity_display()
    print("Class names of all the displayed activities: \n", displayed_activity_info)

    extract_ui()

    click_skip()
    time.sleep(5)

    displayed_activity_after_skip = dumpsys_activity_display()
    print("Class names of all the displayed activities: \n", displayed_activity_after_skip)
    extract_ui()

    delete_shared_preferences(package_name)
    uninstall_app(package_name)


if __name__ == "__main__":
    main()
