TorqueMeasurement
This script processes Excel files from a raw folder, skips the first 49 rows, extracts specific columns, inserts data into a SQLite database, and moves cleaned files to a designated folder.

Prerequisites
Python Installation:
Ensure Python 3.10+ is installed. You can download the latest Python version from the official Python website. 
https://www.python.org/downloads/

Environment Setup:
You will need to set up a virtual environment and install required dependencies using requirements.txt.

Setup Instructions
1. Download and Install Python
Download Python 3.10 or later from Python.org.
Install Python and make sure to enable the "Add Python to PATH" option during installation.

2. Clone or Download the Project
Clone the repository or download the project zip file and extract it.

3. Navigate to the Project Directory
cd /path/to/TorqueMeasurement

4. Create a Virtual Environment
Create a virtual environment to isolate dependencies:
python3 -m venv .venv

5. Activate the Virtual Environment
source .venv/bin/activate

6. Install Dependencies
Use the requirements.txt file to install all necessary dependencies
pip install -r requirements.txt

7. Prepare the Folder Structure
Ensure the following folder structure exists

TorqueMeasurement/
├── Input/
│   ├── raw/       
│   ├── cleaned/ 
│   └── processes/
├── src/
│   ├── file_process_db.py
└── requirements.txt

8. Execute the Script
python src/file_process_db.py

Output Details
Processed Tables:
Data is inserted into the SQLite database, and each table is named in the format <filename>_YYYYMMDD.

Cleaned Files:
Processed Excel files are saved in the Input/cleaned/ folder, named <filename>_YYYYMMDD.xlsx.