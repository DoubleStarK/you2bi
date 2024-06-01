@echo off
set "sourceDir=lib"
set "script_path=%~dp0"
set "target_name=biliup.exe"
set "cookie_file=cookie.json"
echo Current script path is: %script_path%

echo =====Checking system architecture...=====
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    echo =====system arch=AMD64=====
    set "sourceFile=biliup_win_amd64.exe"
) else if "%PROCESSOR_ARCHITECTURE%"=="ARM64" (
    echo =====system arch=ARM64=====
    set "sourceFile=biliup_win_arm64.exe"
) else (
    echo =====system arch=Unknown=====
    exit
)

:: Copy and rename the file if it exists
if not "%sourceFile%"=="" (
    if exist "%script_path%\%sourceDir%\%sourceFile%" (
        copy /y "%script_path%\%sourceDir%\%sourceFile%" "%script_path%\%target_name%"
        echo =====Copied and renamed %sourceFile% to %target_name%=====
    ) else (
        echo =====The file "%script_path%\%sourceDir%\%sourceFile%" does not exist.=====
        exit
    )
) else (
    echo =====Unable to determine system architecture or no matching file found.=====
    exit
)

:: Check login status
if not exist "%script_path%\%cookie_file%" (
    echo =====No %cookie_file%, need login=====
    echo press any key to continue login "%script_path%%target_name%"
    pause
    start "biliup" "%script_path%%target_name%" "login"
) else (
    echo =====You have already logged in=====
)
