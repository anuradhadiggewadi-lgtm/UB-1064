@echo off
:: Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ============================================================
    echo  Administrator privileges required!
    echo ============================================================
    echo.
    echo This script needs Administrator access to configure firewall
    echo.
    echo Requesting Administrator privileges...
    :: Re-launch as administrator
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo ============================================================
echo  ZenStressy - Windows Firewall Configuration
echo ============================================================
echo.
echo Configuring Windows Firewall...
echo.

:: Delete existing rule if it exists
netsh advfirewall firewall delete rule name="ZenStressy Flask Port 5000" >nul 2>&1

:: Add new firewall rule
netsh advfirewall firewall add rule name="ZenStressy Flask Port 5000" dir=in action=allow protocol=TCP localport=5000 enable=yes profile=private,public

if %errorLevel% equ 0 (
    echo.
    echo ============================================================
    echo  SUCCESS! Firewall rule added successfully!
    echo ============================================================
    echo.
    echo You can now access ZenStressy from other devices on your network
    echo.
) else (
    echo.
    echo ============================================================
    echo  ERROR: Could not add firewall rule
    echo ============================================================
    echo.
    echo Please try running this manually as Administrator
    echo.
)

pause

