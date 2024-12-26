:: filepath: /G:/Users/Mostafa/Documents/Bital-Exponential-Graph/setup.bat
@echo off
echo Setting up the environment...

:: Create a virtual environment
python -m venv venv

:: Activate the virtual environment
call venv\Scripts\activate

:: Install required packages
pip install -r requirements.txt

echo Setup complete.
pause