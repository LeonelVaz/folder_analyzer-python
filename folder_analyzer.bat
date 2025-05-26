@echo off
chcp 65001 >nul 2>&1
title Analizador de Carpetas - Iniciando...

REM Obtener la ruta del directorio donde está ubicado el archivo .bat
set "SCRIPT_DIR=%~dp0"

REM Cambiar al directorio del script
cd /d "%SCRIPT_DIR%"

echo.
echo ====================================================
echo           ANALIZADOR DE CARPETAS
echo ====================================================
echo.
echo Iniciando aplicacion...
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo.
    echo Por favor instala Python desde: https://www.python.org/downloads/
    echo Asegurate de marcar "Add Python to PATH" durante la instalacion
    echo.
    pause
    exit /b 1
)

REM Mostrar versión de Python
echo Python detectado:
python --version
echo.

REM Verificar si el archivo Python existe
if not exist "folder_analyzer.py" (
    echo ERROR: No se encontro el archivo 'folder_analyzer.py'
    echo.
    echo Asegurate de que este archivo .bat este en la misma carpeta
    echo que el archivo folder_analyzer.py
    echo.
    pause
    exit /b 1
)

REM Verificar si pyperclip está instalado con mejor manejo
echo Verificando dependencias...
python -c "import pyperclip; print('pyperclip disponible')" >temp_check.txt 2>&1
findstr /C:"pyperclip disponible" temp_check.txt >nul 2>&1
set "pyperclip_status=%errorlevel%"
del temp_check.txt >nul 2>&1

if not "%pyperclip_status%"=="0" (
    echo.
    echo ADVERTENCIA: pyperclip no esta instalado o no funciona correctamente
    echo Esta libreria es necesaria para la funcion de copiar al portapapeles
    echo.
    echo Deseas instalar/reinstalar pyperclip ahora? [S/N]: 
    choice /C SN /N /M "Presiona S para Si o N para No: "
    
    if errorlevel 2 (
        echo.
        echo Continuando sin pyperclip...
        echo La funcion de copiar al portapapeles no estara disponible
        echo.
        goto :run_app
    )
    
    if errorlevel 1 (
        echo.
        echo Instalando pyperclip...
        python -m pip install --upgrade pyperclip
        if errorlevel 1 (
            echo.
            echo ERROR: No se pudo instalar pyperclip
            echo Intentando con pip3...
            pip3 install --upgrade pyperclip
            if errorlevel 1 (
                echo.
                echo ERROR: No se pudo instalar pyperclip con pip3 tampoco
                echo Puedes continuar pero la funcion de copiar al portapapeles no funcionara
                echo.
                pause
            ) else (
                echo.
                echo pyperclip instalado exitosamente con pip3!
                echo.
            )
        ) else (
            echo.
            echo pyperclip instalado exitosamente!
            echo.
        )
    )
) else (
    echo pyperclip ya esta instalado y funcionando correctamente
    echo.
)

:run_app
echo.
echo Iniciando Analizador de Carpetas...
echo.
echo ====================================================
echo.

REM Ejecutar el script de Python
python folder_analyzer.py

REM Verificar si hubo errores
if errorlevel 1 (
    echo.
    echo ====================================================
    echo ERROR: La aplicacion se cerro inesperadamente
    echo ====================================================
    echo.
) else (
    echo.
    echo ====================================================
    echo La aplicacion se cerro correctamente
    echo ====================================================
    echo.
)

echo Presiona cualquier tecla para cerrar esta ventana...
pause >nul