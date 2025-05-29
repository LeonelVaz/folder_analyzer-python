# Reemplazo del .bat para ejecutar folder_analyzer.py con Python 3.10 usando PowerShell

# Configuración Inicial
$Host.UI.RawUI.WindowTitle = "Analizador de Carpetas - Iniciando..."
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8 # Equivalente a chcp 65001

# Definir el comando y argumentos de Python
$PythonExecutable = "py"
$PythonVersionArg = "-3.10" # Argumento para especificar la versión
$PythonScript = "folder_analyzer.py"

# Obtener la ruta del directorio donde está ubicado el archivo .ps1
$ScriptDir = $PSScriptRoot # Equivalente a %~dp0
Set-Location -Path $ScriptDir # Equivalente a cd /d "%SCRIPT_DIR%"

Write-Host ""
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "          ANALIZADOR DE CARPETAS (PowerShell)" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Iniciando aplicación con $PythonExecutable $PythonVersionArg ..."
Write-Host ""

# --- 1. Verificar si Python 3.10 (vía 'py -3.10') está disponible ---
try {
    Write-Host "Verificando la instalación de Python 3.10..."
    & $PythonExecutable $PythonVersionArg --version *> $null # Redirigir stdout y stderr a null para la prueba
    if ($LASTEXITCODE -ne 0) {
        throw "Python 3.10 (a través de '$PythonExecutable $PythonVersionArg') no está disponible o no está en el PATH."
    }
    Write-Host "Python 3.10 detectado:" -ForegroundColor Green
    & $PythonExecutable $PythonVersionArg --version
    Write-Host ""
}
catch {
    Write-Error "ERROR: $($_.Exception.Message)"
    Write-Host ""
    Write-Host "Por favor instala Python 3.10 desde: https://www.python.org/downloads/"
    Write-Host "Asegúrate de que el lanzador 'py.exe' esté instalado y en el PATH."
    Write-Host "Durante la instalación de Python, el lanzador 'py.exe' usualmente se instala por defecto."
    Write-Host ""
    Read-Host -Prompt "Presiona Enter para salir"
    exit 1
}

# --- 2. Verificar si el archivo Python existe ---
if (-not (Test-Path -Path $PythonScript -PathType Leaf)) {
    Write-Error "ERROR: No se encontró el archivo '$PythonScript'"
    Write-Host ""
    Write-Host "Asegúrate de que este archivo .ps1 esté en la misma carpeta"
    Write-Host "que el archivo $PythonScript"
    Write-Host ""
    Read-Host -Prompt "Presiona Enter para salir"
    exit 1
}

# --- 3. Verificar si pyperclip está instalado ---
Write-Host "Verificando dependencias para Python 3.10..."
$pyperclipCheckSuccess = $false
try {
    # Usamos -c para ejecutar un comando corto, redirigiendo errores para capturarlos si es necesario
    $pyperclipOutput = (& $PythonExecutable $PythonVersionArg -c "import pyperclip; print('pyperclip_ok')" 2>&1)

    if ($LASTEXITCODE -eq 0 -and $pyperclipOutput -match "pyperclip_ok") {
        $pyperclipCheckSuccess = $true
        Write-Host "pyperclip ya está instalado y funcionando correctamente con Python 3.10." -ForegroundColor Green
        Write-Host ""
    }
}
catch {
    # Esto podría capturar si el comando python falla catastróficamente,
    # pero la verificación de $LASTEXITCODE y $pyperclipOutput es más precisa para el import.
}

if (-not $pyperclipCheckSuccess) {
    Write-Warning "ADVERTENCIA: pyperclip no está instalado o no funciona correctamente con $PythonExecutable $PythonVersionArg"
    Write-Host "Esta librería es necesaria para la función de copiar al portapapeles."
    Write-Host ""

    $validInput = $false
    while (-not $validInput) {
        $choice = Read-Host -Prompt "Deseas instalar/reinstalar pyperclip para Python 3.10 ahora? [S/N]"
        if ($choice -match "^[SNsn]$") {
            $validInput = $true
        } else {
            Write-Warning "Por favor, introduce S o N."
        }
    }

    if ($choice -eq 's' -or $choice -eq 'S') {
        Write-Host ""
        Write-Host "Instalando pyperclip para Python 3.10..."
        try {
            & $PythonExecutable $PythonVersionArg -m pip install --upgrade pyperclip
            if ($LASTEXITCODE -ne 0) {
                throw "No se pudo instalar pyperclip usando '$PythonExecutable $PythonVersionArg -m pip'."
            }
            Write-Host "pyperclip instalado exitosamente para Python 3.10!" -ForegroundColor Green
            Write-Host ""
        }
        catch {
            Write-Error "ERROR: $($_.Exception.Message)"
            Write-Host "Asegúrate de que pip esté funcionando correctamente para Python 3.10."
            Write-Host "Puedes continuar pero la función de copiar al portapapeles no funcionará."
            Write-Host ""
            Read-Host -Prompt "Presiona Enter para continuar sin pyperclip o cierra esta ventana"
        }
    } else {
        Write-Host ""
        Write-Host "Continuando sin pyperclip..."
        Write-Host "La función de copiar al portapapeles no estará disponible."
        Write-Host ""
    }
}

# --- 4. Ejecutar el script de Python ---
Write-Host ""
Write-Host "Iniciando Analizador de Carpetas con $PythonExecutable $PythonVersionArg ..."
Write-Host ""
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""

# Ejecutar el script y guardar el código de salida
& $PythonExecutable $PythonVersionArg $PythonScript
$AppExitCode = $LASTEXITCODE

# --- 5. Verificar si hubo errores ---
if ($AppExitCode -ne 0) {
    Write-Host ""
    Write-Host "====================================================" -ForegroundColor Red
    Write-Error "ERROR: La aplicación se cerró inesperadamente (Código de salida: $AppExitCode)"
    Write-Host "====================================================" -ForegroundColor Red
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "====================================================" -ForegroundColor Green
    Write-Host "La aplicación se cerró correctamente" -ForegroundColor Green
    Write-Host "====================================================" -ForegroundColor Green
    Write-Host ""
}

Read-Host -Prompt "Presiona Enter para cerrar esta ventana"
exit $AppExitCode