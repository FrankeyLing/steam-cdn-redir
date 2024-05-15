@echo off
set script=%cd%"\main.py"
set python="python"

rem Run the Python script as an administrator
powershell -Command "Start-Process %python% -ArgumentList '%script%' -Verb RunAs"