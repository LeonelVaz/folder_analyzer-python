# folder_analyzer.py

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
from datetime import datetime
import pyperclip

class FolderAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Carpetas")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Variables
        self.selected_folder = tk.StringVar()
        self.output_location = tk.StringVar()
        self.progress_var = tk.DoubleVar()
        self.analysis_result = ""
        
        # Extensiones de archivos soportadas
        self.supported_extensions = {
            '.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.htm', '.css', '.scss', '.sass',
            '.json', '.xml', '.yaml', '.yml', '.md', '.txt', '.csv', '.sql', '.php',
            '.java', '.c', '.cpp', '.h', '.cs', '.rb', '.go', '.rs', '.swift', '.kt',
            '.vue', '.svelte', '.r', '.m', '.sh', '.bat', '.ps1', '.dockerfile'
        }
        
        self.setup_ui()
        
        # Configurar ubicación por defecto (escritorio)
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        self.output_location.set(desktop)
    
    def setup_ui(self):
        # Frame principal con scrollbar
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        main_frame = ttk.Frame(scrollable_frame, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Analizador de Carpetas", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Selección de carpeta
        ttk.Label(main_frame, text="Carpeta a analizar:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        folder_entry = ttk.Entry(main_frame, textvariable=self.selected_folder, width=60)
        folder_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 10), pady=5)
        
        browse_folder_btn = ttk.Button(main_frame, text="Examinar", command=self.browse_folder)
        browse_folder_btn.grid(row=1, column=2, pady=5)
        
        # Selección de ubicación de guardado
        ttk.Label(main_frame, text="Guardar resultado en:").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        output_entry = ttk.Entry(main_frame, textvariable=self.output_location, width=60)
        output_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 10), pady=5)
        
        browse_output_btn = ttk.Button(main_frame, text="Examinar", command=self.browse_output)
        browse_output_btn.grid(row=2, column=2, pady=5)
        
        # Opciones
        options_frame = ttk.LabelFrame(main_frame, text="Opciones", padding="10")
        options_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        options_frame.columnconfigure(0, weight=1)
        
        self.include_subdirs_var = tk.BooleanVar(value=True)
        subdirs_check = ttk.Checkbutton(options_frame, text="Incluir subdirectorios", 
                                       variable=self.include_subdirs_var)
        subdirs_check.grid(row=0, column=0, sticky=tk.W)
        
        self.show_empty_files_var = tk.BooleanVar(value=False)
        empty_files_check = ttk.Checkbutton(options_frame, text="Mostrar archivos vacíos", 
                                           variable=self.show_empty_files_var)
        empty_files_check.grid(row=1, column=0, sticky=tk.W)
        
        self.add_line_numbers_var = tk.BooleanVar(value=False)
        line_numbers_check = ttk.Checkbutton(options_frame, text="Agregar números de línea", 
                                           variable=self.add_line_numbers_var)
        line_numbers_check.grid(row=2, column=0, sticky=tk.W)
        
        self.show_directory_first_var = tk.BooleanVar(value=True)
        directory_first_check = ttk.Checkbutton(options_frame, text="Mostrar directorio de archivos primero", 
                                              variable=self.show_directory_first_var)
        directory_first_check.grid(row=3, column=0, sticky=tk.W)
        
        # Barra de progreso
        self.progress_label = ttk.Label(main_frame, text="")
        self.progress_label.grid(row=4, column=0, columnspan=3, pady=(10, 5))
        
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                          maximum=100, length=500)
        self.progress_bar.grid(row=4, column=0, columnspan=3, pady=5)
        
        # Botones principales
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        self.analyze_btn = ttk.Button(buttons_frame, text="Analizar Carpeta", 
                                     command=self.start_analysis, style='Accent.TButton')
        self.analyze_btn.pack(side=tk.LEFT, padx=5)
        
        self.cancel_btn = ttk.Button(buttons_frame, text="Cancelar", 
                                    command=self.cancel_analysis, state='disabled')
        self.cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Botones de resultado (inicialmente ocultos)
        self.result_frame = ttk.Frame(main_frame)
        self.result_frame.grid(row=6, column=0, columnspan=3, pady=10)
        
        self.save_btn = ttk.Button(self.result_frame, text="Guardar Archivo", 
                                  command=self.save_analysis, state='disabled')
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        self.copy_btn = ttk.Button(self.result_frame, text="Copiar al Portapapeles", 
                                  command=self.copy_to_clipboard, state='disabled')
        self.copy_btn.pack(side=tk.LEFT, padx=5)
        
        # Información
        info_frame = ttk.LabelFrame(main_frame, text="Información", padding="10")
        info_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        info_text = """Extensiones soportadas: .py, .js, .jsx, .ts, .tsx, .html, .css, .json, .md, .txt, .sql, .php, .java, .c, .cpp, .cs, .rb, .go, .vue y más.

Funcionalidades:
• Guardar análisis como archivo de texto
• Copiar análisis directamente al portapapeles
• Mostrar directorio completo de archivos al inicio
• Rutas completas incluyendo carpeta principal"""
        
        info_label = ttk.Label(info_frame, text=info_text, wraplength=600, justify='left')
        info_label.pack()
        
        # Configurar scrolling
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Variable para cancelar análisis
        self.cancel_flag = False
    
    def browse_folder(self):
        folder = filedialog.askdirectory(title="Seleccionar carpeta para analizar")
        if folder:
            self.selected_folder.set(folder)
    
    def browse_output(self):
        folder = filedialog.askdirectory(title="Seleccionar carpeta para guardar el resultado")
        if folder:
            self.output_location.set(folder)
    
    def start_analysis(self):
        if not self.selected_folder.get():
            messagebox.showerror("Error", "Por favor selecciona una carpeta")
            return
        
        if not os.path.exists(self.selected_folder.get()):
            messagebox.showerror("Error", "La carpeta seleccionada no existe")
            return
        
        # Deshabilitar botones y reiniciar estado
        self.analyze_btn.config(state='disabled')
        self.cancel_btn.config(state='normal')
        self.save_btn.config(state='disabled')
        self.copy_btn.config(state='disabled')
        self.cancel_flag = False
        self.analysis_result = ""
        
        # Ejecutar análisis en hilo separado
        thread = threading.Thread(target=self.analyze_folder)
        thread.daemon = True
        thread.start()
    
    def cancel_analysis(self):
        self.cancel_flag = True
        self.progress_label.config(text="Cancelando...")
    
    def analyze_folder(self):
        try:
            folder_path = self.selected_folder.get()
            folder_name = os.path.basename(folder_path)
            
            # Obtener lista de archivos
            self.update_progress("Escaneando archivos...", 10)
            files_to_analyze = self.get_files_list(folder_path)
            
            if self.cancel_flag:
                self.reset_ui()
                return
            
            if not files_to_analyze:
                messagebox.showinfo("Información", "No se encontraron archivos compatibles en la carpeta")
                self.reset_ui()
                return
            
            # Generar análisis en memoria
            self.update_progress(f"Generando análisis de {len(files_to_analyze)} archivos...", 20)
            
            result = []
            
            # Escribir header
            result.append("ANÁLISIS DE CARPETA")
            result.append("=" * 80)
            result.append("")
            result.append(f"Carpeta analizada: {folder_path}")
            result.append(f"Fecha de análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            result.append(f"Total de archivos analizados: {len(files_to_analyze)}")
            result.append(f"Incluye subdirectorios: {'Sí' if self.include_subdirs_var.get() else 'No'}")
            result.append("")
            result.append("=" * 80)
            
            # Mostrar directorio de archivos primero si está habilitado
            if self.show_directory_first_var.get():
                result.append("")
                result.append("DIRECTORIO DE ARCHIVOS")
                result.append("=" * 80)
                
                for file_path in files_to_analyze:
                    rel_path = os.path.relpath(file_path, os.path.dirname(folder_path))
                    result.append(f"• {rel_path}")
                
                result.append("")
                result.append("=" * 80)
                result.append("CONTENIDO DE ARCHIVOS")
                result.append("=" * 80)
            
            # Analizar cada archivo
            for i, file_path in enumerate(files_to_analyze):
                if self.cancel_flag:
                    break
                
                progress = 20 + (i / len(files_to_analyze)) * 70
                filename = os.path.basename(file_path)
                self.update_progress(f"Procesando: {filename}", progress)
                
                self.analyze_file_to_result(result, file_path, folder_path)
            
            if not self.cancel_flag:
                # Footer
                result.append(f"\n{'='*80}")
                result.append("FIN DEL ANÁLISIS")
                result.append(f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                result.append("="*80)
                
                self.analysis_result = "\n".join(result)
                self.update_progress("¡Análisis completado!", 100)
                
                # Habilitar botones de resultado
                self.root.after(0, lambda: [
                    self.save_btn.config(state='normal'),
                    self.copy_btn.config(state='normal')
                ])
                
                messagebox.showinfo("Éxito", "Análisis completado. Ahora puedes guardar el archivo o copiar al portapapeles.")
            else:
                self.update_progress("Análisis cancelado", 0)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el análisis:\n{str(e)}")
        finally:
            self.reset_ui()
    
    def get_files_list(self, folder_path):
        files = []
        
        if self.include_subdirs_var.get():
            for root, dirs, filenames in os.walk(folder_path):
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    if self.is_supported_file(filename):
                        files.append(file_path)
        else:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path) and self.is_supported_file(filename):
                    files.append(file_path)
        
        return sorted(files)
    
    def is_supported_file(self, filename):
        _, ext = os.path.splitext(filename)
        return ext.lower() in self.supported_extensions
    
    def analyze_file_to_result(self, result, file_path, base_folder):
        try:
            # Obtener ruta relativa desde el directorio padre de la carpeta principal
            folder_name = os.path.basename(base_folder)
            parent_dir = os.path.dirname(base_folder)
            rel_path = os.path.relpath(file_path, parent_dir)
            filename = os.path.basename(file_path)
            
            # Escribir información del archivo
            result.append(f"\n{'='*80}")
            result.append(f"Archivo: {filename}")
            result.append(f"Dirección: {rel_path}")
            result.append(f"{'='*80}")
            
            # Leer contenido del archivo
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if not content.strip() and not self.show_empty_files_var.get():
                    result.append("(Archivo vacío - omitido)")
                    return
                
                # Determinar el lenguaje para el resaltado
                extension = os.path.splitext(filename)[1].lower()
                language = self.get_language_from_extension(extension)
                
                result.append(f"Contenido de {filename}:")
                result.append(f"```{language}")
                
                if self.add_line_numbers_var.get():
                    lines = content.split('\n')
                    for i, line in enumerate(lines, 1):
                        result.append(f"{i:4d}: {line}")
                else:
                    result.append(content)
                
                result.append("```")
                
            except UnicodeDecodeError:
                result.append("(Archivo binario - no se puede mostrar el contenido)")
            except Exception as e:
                result.append(f"(Error al leer el archivo: {str(e)})")
                
        except Exception as e:
            result.append(f"Error procesando {file_path}: {str(e)}")
    
    def get_language_from_extension(self, extension):
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'jsx',
            '.ts': 'typescript',
            '.tsx': 'tsx',
            '.html': 'html',
            '.htm': 'html',
            '.css': 'css',
            '.scss': 'scss',
            '.sass': 'sass',
            '.json': 'json',
            '.xml': 'xml',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.md': 'markdown',
            '.txt': 'text',
            '.sql': 'sql',
            '.php': 'php',
            '.java': 'java',
            '.c': 'c',
            '.cpp': 'cpp',
            '.h': 'c',
            '.cs': 'csharp',
            '.rb': 'ruby',
            '.go': 'go',
            '.rs': 'rust',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.vue': 'vue',
            '.svelte': 'svelte'
        }
        return language_map.get(extension, 'text')
    
    def save_analysis(self):
        if not self.analysis_result:
            messagebox.showerror("Error", "No hay análisis para guardar")
            return
        
        try:
            folder_name = os.path.basename(self.selected_folder.get())
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Crear nombre sugerido del archivo
            suggested_name = f"analisis_{folder_name}_{timestamp}.txt"
            
            # Abrir diálogo para guardar archivo
            file_path = filedialog.asksaveasfilename(
                title="Guardar análisis como...",
                initialdir=self.output_location.get(),
                initialfile=suggested_name,
                defaultextension=".txt",
                filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.analysis_result)
                
                messagebox.showinfo("Éxito", f"Archivo guardado exitosamente en:\n{file_path}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el archivo:\n{str(e)}")
    
    def copy_to_clipboard(self):
        if not self.analysis_result:
            messagebox.showerror("Error", "No hay análisis para copiar")
            return
        
        try:
            pyperclip.copy(self.analysis_result)
            messagebox.showinfo("Éxito", "Análisis copiado al portapapeles exitosamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al copiar al portapapeles:\n{str(e)}")
    
    def update_progress(self, text, value):
        self.root.after(0, lambda: [
            self.progress_label.config(text=text),
            self.progress_var.set(value)
        ])
    
    def reset_ui(self):
        self.root.after(0, lambda: [
            self.analyze_btn.config(state='normal'),
            self.cancel_btn.config(state='disabled')
        ])

def main():
    # Verificar si pyperclip está disponible
    try:
        import pyperclip
    except ImportError:
        print("Advertencia: pyperclip no está instalado.")
        print("Para usar la función de copiar al portapapeles, instala pyperclip:")
        print("pip install pyperclip")
        
        # Crear una versión mock de pyperclip
        class MockPyperclip:
            @staticmethod
            def copy(text):
                raise Exception("pyperclip no está instalado. Instala con: pip install pyperclip")
        
        import sys
        sys.modules['pyperclip'] = MockPyperclip()
    
    root = tk.Tk()
    app = FolderAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()