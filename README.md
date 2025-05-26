# 📁 Analizador de Carpetas

Una herramienta simple pero poderosa con interfaz gráfica que permite analizar el contenido completo de una carpeta, generando un documento unificado con la estructura de directorios y el contenido de todos los archivos de código.

## ✨ Características

- **Interfaz gráfica intuitiva** construida con Tkinter
- **Análisis completo** de carpetas con soporte para subdirectorios
- **Múltiples formatos de archivo** soportados (Python, JavaScript, HTML, CSS, JSON, etc.)
- **Directorio de archivos** mostrado al inicio del análisis
- **Rutas completas** incluyendo la carpeta principal
- **Dos opciones de salida**: guardar como archivo o copiar al portapapeles
- **Ubicación personalizable** para guardar archivos
- **Opciones configurables** (subdirectorios, archivos vacíos, números de línea)
- **Barra de progreso** con información en tiempo real
- **Cancelación** del análisis en cualquier momento

## 🚀 Instalación

### Requisitos
- Python 3.6 o superior
- Tkinter (incluido con Python)
- pyperclip (para función de portapapeles)

### Instalación de dependencias
```bash
pip install pyperclip
```

### Descarga
```bash
git clone https://github.com/tu-usuario/folder-analyzer.git
cd folder-analyzer
```

## 💻 Uso

### Ejecutar la aplicación
```bash
python folder_analyzer.py
```

### Pasos de uso
1. **Seleccionar carpeta**: Haz clic en "Examinar" para elegir la carpeta que deseas analizar
2. **Configurar opciones**:
   - ✅ Incluir subdirectorios
   - ✅ Mostrar archivos vacíos
   - ✅ Agregar números de línea
   - ✅ Mostrar directorio de archivos primero
3. **Elegir ubicación de guardado** (opcional)
4. **Analizar**: Haz clic en "Analizar Carpeta"
5. **Guardar resultado**: 
   - **Guardar Archivo**: Crea un archivo .txt en la ubicación elegida
   - **Copiar al Portapapeles**: Copia todo el análisis para pegar donde necesites

## 📋 Formato de salida

El análisis genera un documento estructurado con el siguiente formato:

```
ANÁLISIS DE CARPETA
================================================================================

Carpeta analizada: C:\Users\Usuario\mi-proyecto
Fecha de análisis: 2024-12-07 15:30:45
Total de archivos analizados: 15
Incluye subdirectorios: Sí

================================================================================

DIRECTORIO DE ARCHIVOS
================================================================================
• mi-proyecto\index.js
• mi-proyecto\components\Header.jsx
• mi-proyecto\styles\main.css
• mi-proyecto\utils\helpers.js

================================================================================
CONTENIDO DE ARCHIVOS
================================================================================

Archivo: index.js
Dirección: mi-proyecto\index.js
================================================================================
Contenido de index.js:
```javascript
// Código del archivo aquí
const app = require('./app');
// ...
```

Archivo: Header.jsx
Dirección: mi-proyecto\components\Header.jsx
================================================================================
Contenido de Header.jsx:
```jsx
import React from 'react';
// ...
```
```

## 🔧 Extensiones soportadas

El analizador reconoce y procesa los siguientes tipos de archivo:

**Lenguajes de programación:**
- Python (`.py`)
- JavaScript (`.js`, `.jsx`)
- TypeScript (`.ts`, `.tsx`)
- Java (`.java`)
- C/C++ (`.c`, `.cpp`, `.h`)
- C# (`.cs`)
- Ruby (`.rb`)
- Go (`.go`)
- Rust (`.rs`)
- Swift (`.swift`)
- Kotlin (`.kt`)

**Web y estilos:**
- HTML (`.html`, `.htm`)
- CSS (`.css`, `.scss`, `.sass`)
- Vue (`.vue`)
- Svelte (`.svelte`)

**Datos y configuración:**
- JSON (`.json`)
- XML (`.xml`)
- YAML (`.yaml`, `.yml`)
- CSV (`.csv`)
- Markdown (`.md`)
- Texto (`.txt`)

**Scripts y otros:**
- SQL (`.sql`)
- PHP (`.php`)
- Shell (`.sh`)
- Batch (`.bat`)
- PowerShell (`.ps1`)
- Dockerfile (`.dockerfile`)

## 🛠️ Características técnicas

- **Multihilo**: El análisis se ejecuta en un hilo separado para mantener la interfaz responsiva
- **Manejo de errores**: Gestión robusta de archivos corruptos o binarios
- **Codificación UTF-8**: Soporte completo para caracteres especiales
- **Memoria eficiente**: Procesa archivos uno por uno sin cargar todo en memoria
- **Interfaz escalable**: Ventana redimensionable con scroll automático

## 📸 Casos de uso

- **Documentación de proyectos**: Genera documentación completa de tu código
- **Revisión de código**: Obtén una vista unificada de todos los archivos
- **Backup de código**: Crea copias de seguridad legibles en texto plano
- **Análisis de estructura**: Entiende la organización de proyectos desconocidos
- **Preparación para IA**: Formato perfecto para compartir código con ChatGPT o Claude
