@echo off
cd /d "C:\Users\Director\Documents\ewc_rms"
set DJANGO_SETTINGS_MODULE=ewc_rms.settings
set PYTHONPATH=C:\Users\Director\Documents\ewc_rms;%PYTHONPATH%
call "C:\Users\Director\Documents\venv\Scripts\activate.bat"
python manage.py %*