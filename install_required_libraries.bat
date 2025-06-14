@echo off
setlocal

rem Try to find QGIS in Program Files
set "QGISPATH="
for /d %%D in ("%ProgramFiles%\QGIS*") do (
    set "QGISPATH=%%~fD"
    goto :found
)
rem If not found, try Program Files (x86)
for /d %%D in ("%ProgramFiles(x86)%\QGIS*") do (
    set "QGISPATH=%%~fD"
    goto :found
)

echo QGIS installation not found.
exit /B 1

:found
echo Found QGIS at: "%QGISPATH%"
echo Initializing QGIS Python environment...
call "%QGISPATH%\bin\o4w_env.bat"

echo Installing dependencies from requirements.txt...
python -m pip install -r "%~dp0requirements.txt"

echo Dependencies installed successfully.