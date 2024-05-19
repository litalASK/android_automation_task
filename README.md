# Android automation task

Using Androguard and ADB

## Installation

1. Clone the repository:
~~~~
git clone https://github.com/litalASK/android_automation_task.git
~~~~

2. Install dependencies:
~~~~
pip install -r requirements.txt
~~~~

## Usage

1. For part 1 in the task, run the command:
~~~~
python3 manifest_scraping.py .\task_apk.apk
~~~~

2. For part 2 in the task, run the command:
~~~~
python3 app.py .\task_apk.apk
~~~~

> [!NOTE]
> The first argument is the file name, and second is the apk file