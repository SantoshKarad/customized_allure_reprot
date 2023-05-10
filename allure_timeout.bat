@echo off
echo Please enter the path to the report folder:
set /p reportPath=
set serverPort=12345
start cmd /k "allure serve --port %serverPort% %reportPath% && exit"
timeout /t 90 /nobreak
for /f "tokens=5" %%a in ('netstat -aon ^| findstr 0.0:%serverPort%') do taskkill /pid %%a /f
