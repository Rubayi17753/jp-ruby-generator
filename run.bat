@echo off
set PYTHONPATH=%~dp0
python -m src.mecab_rubygen "%~1"
pause