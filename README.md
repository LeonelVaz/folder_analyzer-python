# 📁 Analizador de Carpetas

Una herramienta avanzada con interfaz gráfica que permite analizar el contenido completo de una carpeta, generando un documento unificado con la estructura de directorios y el contenido de todos los archivos de código, con opciones de personalización y persistencia.

## ✨ Características Clave

- **Interfaz gráfica moderna e intuitiva** construida con Tkinter, organizada en pestañas.
- **Análisis completo** de carpetas con soporte para subdirectorios.
- **Múltiples formatos de archivo** soportados (Python, JavaScript, HTML, CSS, JSON, etc.).
- **Personalización del Análisis**:
  - Incluir/excluir subdirectorios.
  - Mostrar/ocultar archivos vacíos.
  - Agregar/omitir números de línea en el contenido.
  - Mostrar directorio de archivos al inicio del reporte.
- **Gestión de Elementos Ignorados**:
  - Añadir archivos o carpetas específicas a una lista de ignorados.
  - Interfaz para gestionar la lista (añadir por examinador, texto, eliminar, limpiar).
- **Persistencia de Configuración**:
  - Guarda automáticamente la última carpeta analizada, la última ubicación de guardado y la lista de ignorados (configurable por el usuario).
  - Guarda el estado de las opciones de análisis.
- **Salida Flexible**:
  - Guardar el análisis como archivo de texto.
  - Copiar todo el análisis directamente al portapapeles.
- **Experiencia de Usuario Mejorada**:
  - **Notificaciones en la UI**: Mensajes no intrusivos para operaciones exitosas (análisis, guardado, copiado).
  - **Contador de tiempo desde último análisis**: Indicador visual (verde/naranja/rojo) de cuán reciente es el análisis actual.
  - Barra de progreso con información en tiempo real.
  - Cancelación del análisis en cualquier momento.
- **Rutas completas** incluyendo la carpeta principal en el reporte.
- **Directorio de archivos** opcionalmente mostrado al inicio del análisis.

## 🚀 Instalación

### Requisitos

- **Python 3.10**: Específicamente la versión 3.10. Se recomienda usar el lanzador `py.exe` de Python para Windows (`py -3.10`).
- **Tkinter**: Generalmente incluido con Python.
- **`pyperclip`**: Para la función de copiar al portapapeles.
- **(Windows)** PowerShell: Para el script de inicio recomendado. PowerShell 5.1 o superior está generalmente disponible en Windows 10/11.

### Instalación de dependencias

Si necesitas instalar `pyperclip` manualmente para Python 3.10:

```bash
py -3.10 -m pip install pyperclip
```

````

El script de inicio para Windows intentará guiarte en este proceso si es necesario.

### Descarga

```bash
git clone https://github.com/LeonelVaz/folder_analyzer-python.git
cd folder_analyzer-python
```

O descarga los archivos necesarios directamente del repositorio:

- `folder_analyzer.py` (el script principal de la aplicación)
- `run_analyzer.ps1` (el script de PowerShell que gestiona la ejecución)
- `iniciar.bat` (el lanzador para Windows que ejecuta el script de PowerShell)

## 💻 Uso

### Método 1: Ejecutar con archivo `iniciar.bat` (Recomendado para Windows)

Este método utiliza un script de PowerShell (`run_analyzer.ps1`) gestionado por un archivo `.bat` para una experiencia de usuario más fluida, incluyendo la verificación de Python 3.10 y dependencias.

1.  **Descarga los archivos**: Asegúrate de tener `folder_analyzer.py`, `run_analyzer.ps1`, e `iniciar.bat` en la misma carpeta.
2.  **Ejecuta el `.bat`**: Doble clic en `iniciar.bat`.
3.  El script `iniciar.bat` lanzará `run_analyzer.ps1`, el cual:
    - ✅ Verificará que Python 3.10 (a través de `py -3.10`) esté disponible.
    - ✅ Detectará si `pyperclip` está instalado y funcional para Python 3.10.
    - ✅ Ofrecerá instalar/reinstalar `pyperclip` si no está presente o no funciona.
    - ✅ Iniciará la aplicación `folder_analyzer.py` usando Python 3.10.

### Método 2: Ejecutar directamente con PowerShell (Alternativa para Windows)

Si prefieres, puedes ejecutar el script de PowerShell directamente:

1.  Abre una ventana de PowerShell.
2.  Navega hasta el directorio donde se encuentran los archivos: `cd "ruta\a\tu\carpeta"`.
3.  Ejecuta el script: `.\run_analyzer.ps1`.
    - _Nota_: Si no usas el `iniciar.bat` (que utiliza `-ExecutionPolicy Bypass`), es posible que necesites ajustar tu política de ejecución de PowerShell. Si encuentras un error relacionado con la política de ejecución, abre PowerShell como Administrador y ejecuta `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` o `Set-ExecutionPolicy Unrestricted -Scope CurrentUser` (menos seguro).

### Método 3: Ejecutar manualmente con Python (Multiplataforma)

Este método requiere que ya tengas Python 3.10 y `pyperclip` configurados correctamente.

1.  Abre tu terminal o línea de comandos.
2.  Navega al directorio del script.
3.  Ejecuta:
    ```bash
    py -3.10 folder_analyzer.py
    ```
    (En Linux/macOS, si `python3.10` está en tu PATH, puedes usar `python3.10 folder_analyzer.py`)

### Pasos de uso de la Aplicación

Una vez iniciada la aplicación:

1.  **Pestaña "Principal"**:

    - **Seleccionar carpeta a analizar**: Usa "Examinar" o escribe la ruta. Puedes marcar "P" (Persistir) para recordar esta carpeta.
    - **Elegir ubicación de guardado**: Similar al anterior, para donde se sugerirá guardar los reportes.
    - **Configurar elementos a ignorar**:
      - Escribe el nombre de un archivo (ej: `config.log`) o carpeta (ej: `node_modules/`) y usa los botones "Añadir Archivo", "Añadir Carpeta" o "Añadir Texto".
      - Puedes marcar "Persistir lista de ignorados".
    - **Analizar**: Haz clic en "🚀 Analizar Carpeta". Observa el contador de tiempo y la barra de progreso.
    - **Resultados**:
      - **💾 Guardar Archivo**: Crea un archivo `.txt`.
      - **📋 Copiar al Portapapeles**: Copia todo el análisis.
      - Las operaciones exitosas mostrarán una notificación en la esquina inferior derecha.

2.  **Pestaña "Opciones"**:
    - Configura cómo se realiza el análisis (subdirectorios, archivos vacíos, números de línea, etc.). Estas opciones también se guardan.

## 📋 Formato de salida

El análisis genera un documento estructurado similar al siguiente:

````

# ANÁLISIS DE CARPETA

Carpeta analizada: C:\Users\Usuario\mi-proyecto
Fecha de análisis: 2024-12-07 15:30:45
Total de archivos analizados: 15
Incluye subdirectorios: Sí
Mostrar archivos vacíos: No
Agregar números de línea: Sí
Mostrar directorio primero: Sí

## ELEMENTOS IGNORADOS (si los hay)

Archivos:
• .env
• temp.log
Carpetas:
• node_modules/
• .git/

================================================================================

# DIRECTORIO DE ARCHIVOS (si la opción está activa)

• mi-proyecto\index.js
• mi-proyecto\components\Header.jsx
...

================================================================================
CONTENIDO DE ARCHIVOS
================================================================================

Archivo: index.js
Ruta: mi-proyecto\index.js

---

Contenido (javascript):

```javascript
1   | // Código del archivo aquí
2   | const app = require('./app');
...
```

```

## 🔧 Extensiones soportadas

El analizador reconoce y procesa una amplia gama de tipos de archivo, incluyendo (pero no limitado a):

**Lenguajes de programación:**
- Python (`.py`), JavaScript (`.js`, `.jsx`), TypeScript (`.ts`, `.tsx`), Java (`.java`), C/C++ (`.c`, `.cpp`, `.h`), C# (`.cs`), Ruby (`.rb`), Go (`.go`), Rust (`.rs`), Swift (`.swift`), Kotlin (`.kt`), PHP (`.php`)

**Web y estilos:**
- HTML (`.html`, `.htm`), CSS (`.css`, `.scss`, `.sass`), Vue (`.vue`), Svelte (`.svelte`)

**Datos y configuración:**
- JSON (`.json`), XML (`.xml`), YAML (`.yaml`, `.yml`), CSV (`.csv`), Markdown (`.md`), Texto (`.txt`)

**Scripts y otros:**
- SQL (`.sql`), Shell (`.sh`), Batch (`.bat`), PowerShell (`.ps1`), Dockerfile (`.dockerfile`)

## 🛠️ Características técnicas

- **Multihilo**: El análisis se ejecuta en un hilo separado para mantener la interfaz responsiva.
- **Manejo de errores**: Gestión de archivos con codificación inesperada (reemplaza caracteres problemáticos).
- **Codificación UTF-8**: Soporte para caracteres especiales en la lectura y escritura de archivos.
- **Configuración Persistente**: Las preferencias del usuario se guardan en un archivo JSON en el directorio home (`~/.folder_analyzer_config_v3.json`).
- **Interfaz Moderna**: Uso de `ttk` para widgets temáticos y una organización mejorada.
- **Notificaciones No Intrusivas**: Feedback al usuario sin interrumpir el flujo de trabajo.
- **Lanzador de PowerShell para Windows**: El archivo `run_analyzer.ps1` (ejecutado por `iniciar.bat`) gestiona la comprobación de Python 3.10 y `pyperclip`, mejorando la experiencia de inicio.
- **Uso del lanzador de Python (`py.exe`)**: Para asegurar la ejecución con Python 3.10 en Windows.

## 🔧 Solución de problemas

### Error "pyperclip no encontrado" o similar
- Si estás utilizando el método de inicio recomendado (`iniciar.bat`), el script intentará ayudarte.
- Si lo ejecutas manualmente, asegúrate de que `pyperclip` esté instalado en el entorno Python 3.10 que estás usando: `py -3.10 -m pip install --upgrade pyperclip`.
- En Linux, `pyperclip` puede requerir `xclip` o `xsel`: `sudo apt-get install xclip` o `sudo apt-get install xsel`.

### Python 3.10 no encontrado (al usar `iniciar.bat` o `run_analyzer.ps1`)
- El script busca `py -3.10`. Asegúrate de que:
    1.  Python 3.10 esté instalado desde [python.org](https://www.python.org/downloads/).
    2.  El lanzador de Python para Windows (`py.exe`) esté instalado y en tu PATH. Esto generalmente se incluye por defecto con la instalación de Python en Windows. Marca la opción "Install launcher for all users (recommended)" y "Add Python to PATH" durante la instalación.

### Problemas con la Política de Ejecución de PowerShell (al ejecutar `.ps1` directamente)
- Si intentas ejecutar `run_analyzer.ps1` directamente (sin el `iniciar.bat`) y obtienes un error sobre la política de ejecución, abre PowerShell como Administrador y ejecuta `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`. Esto solo necesita hacerse una vez. El `iniciar.bat` evita este problema usando `-ExecutionPolicy Bypass` para su sesión.

### Problemas de codificación de caracteres
- La aplicación usa UTF-8 por defecto. Si encuentras problemas con archivos específicos, verifica su codificación original.

## 📦 Archivos incluidos

- `folder_analyzer.py` - La aplicación principal en Python.
- `run_analyzer.ps1` - Script de PowerShell para gestionar el entorno y la ejecución en Windows.
- `iniciar.bat` - Script de inicio simplificado para Windows que ejecuta `run_analyzer.ps1`.
- `README.md` - Esta documentación.

## 📸 Casos de uso

- **Documentación de proyectos**: Genera un snapshot completo del código fuente.
- **Revisión de código**: Obtén una vista unificada de todos los archivos para facilitar la revisión.
- **Backup de código**: Crea copias de seguridad legibles en formato de texto plano.
- **Análisis de estructura**: Entiende rápidamente la organización de proyectos desconocidos.
- **Preparación para IA**: Formato ideal para compartir bases de código con modelos de lenguaje grandes (Claude, Gemini, ChatGPT, etc.), especialmente con la capacidad de ignorar directorios como `node_modules/
```
