@echo off
REM Obtener la ruta del directorio donde está ubicado el archivo .bat
set "SCRIPT_DIR=%~dp0"

REM Ejecutar el script de PowerShell.
REM -NoProfile: No carga el perfil de PowerShell (más rápido).
REM -ExecutionPolicy Bypass: Permite ejecutar el script sin cambiar la política global (solo para esta ejecución).
REM -File: Especifica el archivo de script a ejecutar.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%folder_analyzer_powershell.ps1"

REM Opcional: Pausar si quieres ver alguna salida de error del propio powershell.exe
REM if errorlevel 1 (
REM     echo.
REM     echo Hubo un error al intentar lanzar el script de PowerShell.
REM     pause
REM )