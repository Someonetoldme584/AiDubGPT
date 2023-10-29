@echo off
color a
type "intro.txt"

call conda activate coquitts
python main.py
pause