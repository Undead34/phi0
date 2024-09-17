@REM Setup the python proyect, create .venv and intall dependencies with pip
@echo off

@REM Create virtual environment
python -m venv .venv

@REM Activate virtual environment
.venv\Scripts\activate

@REM Install dependencies
pip install -r requirements.txt