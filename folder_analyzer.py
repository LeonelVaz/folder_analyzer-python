# folder_analyzer.py

import tkinter as tk
from tkinter import filedialog, messagebox, ttk # messagebox se mantiene para errores y confirmaciones
import os
import threading
from datetime import datetime
import pyperclip 
import json
import time

class FolderAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Carpetas Pro")
        self.root.geometry("900x800") 
        self.root.resizable(True, True)
        self.root.tk_setPalette(background='#ECECEC')

        self.font_title = ('Segoe UI', 18, 'bold')
        self.font_header = ('Segoe UI', 12, 'bold')
        self.font_normal = ('Segoe UI', 10)
        self.font_small = ('Segoe UI', 9)
        self.font_small_italic = ('Segoe UI', 9, 'italic')
        self.font_timer = ('Consolas', 10)

        self.selected_folder = tk.StringVar()
        self.output_location = tk.StringVar()
        self.progress_var = tk.DoubleVar()
        self.analysis_result = ""
        self.ignored_items = set()
        self.config_file = os.path.join(os.path.expanduser("~"), ".folder_analyzer_config_v3.json")

        self.supported_extensions = {
            '.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.htm', '.css', '.scss', '.sass',
            '.json', '.xml', '.yaml', '.yml', '.md', '.txt', '.csv', '.sql', '.php',
            '.java', '.c', '.cpp', '.h', '.cs', '.rb', '.go', '.rs', '.swift', '.kt',
            '.vue', '.svelte', '.r', '.m', '.sh', '.bat', '.ps1', '.dockerfile'
        }

        self.last_analysis_timestamp = None
        self.timer_label_var = tk.StringVar(value="Último análisis: N/A")
        self.timer_update_job = None

        self.persist_selected_folder_var = tk.BooleanVar(value=True)
        self.persist_output_location_var = tk.BooleanVar(value=True)
        self.persist_ignored_items_var = tk.BooleanVar(value=True)
        
        self.include_subdirs_var = tk.BooleanVar(value=True)
        self.show_empty_files_var = tk.BooleanVar(value=False)
        self.add_line_numbers_var = tk.BooleanVar(value=False)
        self.show_directory_first_var = tk.BooleanVar(value=True)

        self.setup_styles()
        self.setup_ui() 
        
        self.loading_config = True
        self.load_config()
        self.loading_config = False

        self.selected_folder.trace_add("write", self.on_selected_folder_change)
        self.output_location.trace_add("write", self.on_output_location_change)
        self.include_subdirs_var.trace_add("write", lambda *a: self.save_config_if_not_loading())
        self.show_empty_files_var.trace_add("write", lambda *a: self.save_config_if_not_loading())
        self.add_line_numbers_var.trace_add("write", lambda *a: self.save_config_if_not_loading())
        self.show_directory_first_var.trace_add("write", lambda *a: self.save_config_if_not_loading())

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self._notification_job = None

    def save_config_if_not_loading(self):
        if not self.loading_config:
            self.save_config()

    def setup_styles(self):
        style = ttk.Style()
        available_themes = style.theme_names()
        if 'clam' in available_themes: style.theme_use('clam')
        elif 'vista' in available_themes: style.theme_use('vista')
        
        style.configure('.', font=self.font_normal, background='#ECECEC', foreground='#333333')
        style.configure('TLabel', font=self.font_normal, padding=(0, 2), background='#ECECEC')
        style.configure('TButton', font=self.font_normal, padding=(8, 4))
        style.configure('Accent.TButton', font=(self.font_normal[0], self.font_normal[1], 'bold'), padding=(10, 6))
        style.configure('Small.TCheckbutton', font=self.font_small, background='#ECECEC')
        style.configure('TCheckbutton', background='#ECECEC')
        style.configure('TEntry', font=self.font_normal, padding=(5, 3))
        style.configure('TListbox', font=self.font_normal)
        style.configure('TNotebook', tabmargins=[2, 5, 2, 0], background='#ECECEC')
        style.configure('TNotebook.Tab', font=(self.font_normal[0], self.font_normal[1]+1, 'bold'), padding=(12, 6), compound='left')
        style.configure('Header.TLabel', font=self.font_header, padding=(0, 5), background='#ECECEC')
        style.configure('TLabelframe', font=self.font_header, padding=10, relief='groove', borderwidth=1, background='#ECECEC')
        style.configure('TLabelframe.Label', font=self.font_header, foreground='#222222', background='#ECECEC')
        style.configure('Background.TFrame', background='#ECECEC')
        style.configure('Notification.TLabel', font=self.font_small, padding=(8, 5), 
                        relief='solid', borderwidth=1)

    def on_closing(self):
        if self.timer_update_job: self.root.after_cancel(self.timer_update_job)
        if self._notification_job: self.root.after_cancel(self._notification_job)
        self.save_config(); self.root.destroy()

    def on_selected_folder_change(self, *a):
        if not self.loading_config and self.persist_selected_folder_var.get(): self.save_config()

    def on_output_location_change(self, *a):
        if not self.loading_config and self.persist_output_location_var.get(): self.save_config()

    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root, padding="10 10 10 10")
        self.notebook.pack(expand=True, fill='both')

        tab_principal_outer = ttk.Frame(self.notebook, padding="0", style='Background.TFrame')
        self.notebook.add(tab_principal_outer, text=' Principal ')
        
        canvas = tk.Canvas(tab_principal_outer, bg='#ECECEC', highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab_principal_outer, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Background.TFrame')

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def frame_width(event): canvas.itemconfig(canvas_window, width = event.width)
        canvas.bind('<Configure>', frame_width)

        tab_principal_outer.columnconfigure(0, weight=1); tab_principal_outer.rowconfigure(0, weight=1)
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        main_content_frame = ttk.Frame(scrollable_frame, padding="20 20 25 20", style='Background.TFrame')
        main_content_frame.pack(expand=True, fill='x')
        
        app_title_label = ttk.Label(main_content_frame, text="Analizador de Carpetas Pro", font=self.font_title, style='Header.TLabel')
        app_title_label.pack(pady=(0, 25), anchor='w')

        paths_frame = ttk.LabelFrame(main_content_frame, text="Ubicaciones Clave")
        paths_frame.pack(fill="x", expand=True, pady=(0, 20))
        paths_frame.columnconfigure(1, weight=1)

        ttk.Label(paths_frame, text="Carpeta a analizar:").grid(row=0, column=0, sticky=tk.W, pady=(10,8), padx=10)
        folder_entry = ttk.Entry(paths_frame, textvariable=self.selected_folder, width=60)
        folder_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=(10,8))
        persist_selected_cb = ttk.Checkbutton(paths_frame, text="📌", variable=self.persist_selected_folder_var, command=self.save_config, style='Small.TCheckbutton')
        persist_selected_cb.grid(row=0, column=2, padx=(0,3), pady=(10,8), sticky=tk.W)
        self.create_tooltip(persist_selected_cb, "Persistir esta ruta")
        browse_folder_btn = ttk.Button(paths_frame, text="📂 Examinar", command=self.browse_folder, compound=tk.LEFT)
        browse_folder_btn.grid(row=0, column=3, pady=(10,8), padx=(0,10))

        ttk.Label(paths_frame, text="Guardar resultado en:").grid(row=1, column=0, sticky=tk.W, pady=(8,10), padx=10)
        output_entry = ttk.Entry(paths_frame, textvariable=self.output_location, width=60)
        output_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=(8,10))
        persist_output_cb = ttk.Checkbutton(paths_frame, text="📌", variable=self.persist_output_location_var, command=self.save_config, style='Small.TCheckbutton')
        persist_output_cb.grid(row=1, column=2, padx=(0,3), pady=(8,10), sticky=tk.W)
        self.create_tooltip(persist_output_cb, "Persistir ruta de guardado")
        browse_output_btn = ttk.Button(paths_frame, text="📂 Examinar", command=self.browse_output, compound=tk.LEFT)
        browse_output_btn.grid(row=1, column=3, pady=(8,10), padx=(0,10))
        
        ttk.Separator(main_content_frame, orient='horizontal').pack(fill='x', pady=20, padx=5)

        ignore_frame = ttk.LabelFrame(main_content_frame, text="Elementos a Ignorar")
        ignore_frame.pack(fill="x", expand=True, pady=(0, 20))
        ignore_top_frame = ttk.Frame(ignore_frame, style='Background.TFrame')
        ignore_top_frame.pack(fill='x', pady=(10,10), padx=10)
        ignore_top_frame.columnconfigure(0, weight=1)
        self.ignore_entry = ttk.Entry(ignore_top_frame, width=45)
        self.ignore_entry.grid(row=0, column=0, sticky="ew", padx=(0,10), ipady=2)
        self.ignore_entry.bind("<Return>", lambda e: self.add_ignore_item())
        ignore_buttons_frame = ttk.Frame(ignore_top_frame, style='Background.TFrame')
        ignore_buttons_frame.grid(row=0, column=1, sticky='e')
        add_file_btn = ttk.Button(ignore_buttons_frame, text="Archivo", command=self.browse_file_to_ignore)
        add_file_btn.pack(side=tk.LEFT, padx=(0,4))
        add_folder_btn = ttk.Button(ignore_buttons_frame, text="Carpeta", command=self.browse_folder_to_ignore)
        add_folder_btn.pack(side=tk.LEFT, padx=(0,4))
        add_manual_btn = ttk.Button(ignore_buttons_frame, text="Texto", command=self.add_ignore_item)
        add_manual_btn.pack(side=tk.LEFT)
        persist_ignored_cb = ttk.Checkbutton(ignore_top_frame, text="Persistir lista", variable=self.persist_ignored_items_var, command=self.save_config, style='Small.TCheckbutton')
        persist_ignored_cb.grid(row=0, column=2, padx=(15,0), sticky='e')
        self.create_tooltip(persist_ignored_cb, "Guardar lista de ignorados")
        listbox_frame = ttk.Frame(ignore_frame, style='Background.TFrame')
        listbox_frame.pack(fill='both', expand=True, padx=10, pady=(0,5))
        listbox_frame.columnconfigure(0, weight=1); listbox_frame.rowconfigure(0, weight=1)
        self.ignored_listbox = tk.Listbox(listbox_frame, height=6, selectmode=tk.EXTENDED, relief='solid', borderwidth=1, font=self.font_small)
        self.ignored_listbox.grid(row=0, column=0, sticky="nsew")
        ignored_scrollbar_y = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.ignored_listbox.yview)
        ignored_scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.ignored_listbox.configure(yscrollcommand=ignored_scrollbar_y.set)
        ignore_list_buttons_frame = ttk.Frame(ignore_frame, style='Background.TFrame')
        ignore_list_buttons_frame.pack(fill='x', pady=(5,10), padx=10)
        remove_btn = ttk.Button(ignore_list_buttons_frame, text="Eliminar", command=self.remove_ignore_items)
        remove_btn.pack(side=tk.LEFT, padx=(0,5))
        clear_btn = ttk.Button(ignore_list_buttons_frame, text="Limpiar", command=self.clear_ignore_list)
        clear_btn.pack(side=tk.LEFT)
        format_info_label = ttk.Label(ignore_list_buttons_frame, text=" (ej: nombre.ext, carpeta/)", font=self.font_small_italic)
        format_info_label.pack(side=tk.LEFT, padx=(10,0), pady=(2,0))

        ttk.Separator(main_content_frame, orient='horizontal').pack(fill='x', pady=20, padx=5)

        actions_frame = ttk.Frame(main_content_frame, style='Background.TFrame')
        actions_frame.pack(fill="x", expand=True)
        actions_frame.columnconfigure(0, weight=1) 
        status_bar_frame = ttk.Frame(actions_frame, style='Background.TFrame')
        status_bar_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0,15))
        status_bar_frame.columnconfigure(1, weight=1)
        self.timer_label = ttk.Label(status_bar_frame, textvariable=self.timer_label_var, font=self.font_timer)
        self.timer_label.grid(row=0, column=0, sticky=tk.W, padx=(0,20)) 
        self.progress_label = ttk.Label(status_bar_frame, text="Esperando acción...", font=self.font_small)
        self.progress_label.grid(row=0, column=1, sticky=tk.EW, padx=(0,10)) 
        self.progress_bar = ttk.Progressbar(status_bar_frame, variable=self.progress_var, maximum=100, length=220) 
        self.progress_bar.grid(row=0, column=2, sticky=tk.E)
        buttons_control_frame = ttk.Frame(actions_frame, style='Background.TFrame')
        buttons_control_frame.grid(row=1, column=0, sticky='ew', pady=(0,10))
        self.analyze_btn = ttk.Button(buttons_control_frame, text="🚀 Analizar Carpeta", command=self.start_analysis, style='Accent.TButton', compound=tk.LEFT)
        self.analyze_btn.pack(side=tk.LEFT, padx=(0,8))
        self.cancel_btn = ttk.Button(buttons_control_frame, text="❌ Cancelar", command=self.cancel_analysis, state='disabled', compound=tk.LEFT)
        self.cancel_btn.pack(side=tk.LEFT, padx=(0,25))
        self.save_btn = ttk.Button(buttons_control_frame, text="💾 Guardar", command=self.save_analysis, state='disabled', compound=tk.LEFT)
        self.save_btn.pack(side=tk.LEFT, padx=(0,8))
        self.copy_btn = ttk.Button(buttons_control_frame, text="📋 Copiar", command=self.copy_to_clipboard, state='disabled', compound=tk.LEFT)
        self.copy_btn.pack(side=tk.LEFT)

        def _on_mousewheel_scroll(event, scroll_canvas):
            direction = 0
            if event.num == 5 or event.delta < 0: direction = 1
            if event.num == 4 or event.delta > 0: direction = -1
            scroll_canvas.yview_scroll(direction, "units")
        for widget_to_bind in [canvas, scrollable_frame, main_content_frame, paths_frame, ignore_frame, actions_frame, status_bar_frame, buttons_control_frame]:
            widget_to_bind.bind("<MouseWheel>", lambda e, c=canvas: _on_mousewheel_scroll(e, c))
            widget_to_bind.bind("<Button-4>", lambda e, c=canvas: _on_mousewheel_scroll(e, c))
            widget_to_bind.bind("<Button-5>", lambda e, c=canvas: _on_mousewheel_scroll(e, c))
        scrollable_frame.bind("<Enter>", lambda e: canvas.focus_set())

        tab_opciones = ttk.Frame(self.notebook, padding="20", style='Background.TFrame')
        self.notebook.add(tab_opciones, text=' Opciones ')
        options_analysis_frame = ttk.LabelFrame(tab_opciones, text="Configuración del Análisis")
        options_analysis_frame.pack(expand=False, fill="x", padx=10, pady=10)
        subdirs_check = ttk.Checkbutton(options_analysis_frame, text="Incluir subdirectorios", variable=self.include_subdirs_var)
        subdirs_check.grid(row=0, column=0, sticky=tk.W, pady=6, padx=10)
        empty_files_check = ttk.Checkbutton(options_analysis_frame, text="Mostrar archivos vacíos", variable=self.show_empty_files_var)
        empty_files_check.grid(row=1, column=0, sticky=tk.W, pady=6, padx=10)
        line_numbers_check = ttk.Checkbutton(options_analysis_frame, text="Agregar números de línea al contenido", variable=self.add_line_numbers_var)
        line_numbers_check.grid(row=2, column=0, sticky=tk.W, pady=6, padx=10)
        directory_first_check = ttk.Checkbutton(options_analysis_frame, text="Mostrar directorio de archivos al inicio del reporte", variable=self.show_directory_first_var)
        directory_first_check.grid(row=3, column=0, sticky=tk.W, pady=6, padx=10)
        options_info_label = ttk.Label(options_analysis_frame, text="\nNota: Estas opciones se guardan automáticamente.", font=self.font_small_italic)
        options_info_label.grid(row=4, column=0, sticky=tk.W, pady=(15,5), padx=10)
        
        self.notification_label = ttk.Label(self.root, text="", style='Notification.TLabel', anchor='center')

        self.cancel_flag = False
        self.update_timer_display() 

    def show_notification(self, message, duration=3000, msg_type="info"):
        if self._notification_job:
            self.root.after_cancel(self._notification_job)

        if msg_type == "success": bg_color, fg_color = "#D4EDDA", "#155724"
        elif msg_type == "error": bg_color, fg_color = "#F8D7DA", "#721C24"
        else: bg_color, fg_color = "#D1ECF1", "#0C5460"
        
        self.notification_label.config(text=message, background=bg_color, foreground=fg_color)
        
        self.root.update_idletasks()
        label_width_req = self.notification_label.winfo_reqwidth()
        
        max_width_allowed = self.root.winfo_width() * 0.6 # Max 60% de la ventana
        actual_width = min(label_width_req + 20, max_width_allowed) # +20 para padding interno
        
        if label_width_req > max_width_allowed:
            self.notification_label.config(wraplength=int(max_width_allowed - 30)) # -30 para padding y borde
            self.root.update_idletasks()
            actual_width = self.notification_label.winfo_reqwidth() + 20 # Recalcular con wrap
            
        label_height = self.notification_label.winfo_reqheight()

        x_pos = self.root.winfo_width() - actual_width - 20 
        y_pos = self.root.winfo_height() - label_height - 20
        
        self.notification_label.place(x=x_pos, y=y_pos, width=actual_width, height=label_height)
        self.notification_label.lift()

        self._notification_job = self.root.after(duration, self.hide_notification)

    def hide_notification(self):
        if hasattr(self, 'notification_label') and self.notification_label.winfo_exists():
            self.notification_label.place_forget()
        self._notification_job = None

    def create_tooltip(self, widget, text):
        tooltip = None
        def enter(event):
            nonlocal tooltip
            if tooltip is not None: tooltip.destroy()
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            label = tk.Label(tooltip, text=text, background="#FFFFE0", relief="solid", borderwidth=1, 
                             font=self.font_small, justify="left", wraplength=200)
            label.pack(ipadx=4, ipady=4)
            x = widget.winfo_rootx() + widget.winfo_width() // 2 - tooltip.winfo_reqwidth() // 2
            y = widget.winfo_rooty() + widget.winfo_height() + 3
            sw, sh = widget.winfo_screenwidth(), widget.winfo_screenheight()
            if x + tooltip.winfo_reqwidth() > sw: x = sw - tooltip.winfo_reqwidth() - 5
            if y + tooltip.winfo_reqheight() > sh: y = widget.winfo_rooty() - tooltip.winfo_reqheight() - 3
            if x < 5: x = 5
            if y < 5: y = 5
            tooltip.wm_geometry(f"+{int(x)}+{int(y)}")
        _tooltip_leave_job = None
        def leave(event):
            nonlocal tooltip, _tooltip_leave_job
            if _tooltip_leave_job: widget.after_cancel(_tooltip_leave_job)
            _tooltip_leave_job = widget.after(150, destroy_tooltip_safely)
        def destroy_tooltip_safely():
            nonlocal tooltip
            if tooltip and tooltip.winfo_exists():
                tooltip.destroy()
                tooltip = None
        widget.bind("<Enter>", enter, add="+")
        widget.bind("<Leave>", leave, add="+")

    def update_timer_display(self):
        if self.timer_update_job: self.root.after_cancel(self.timer_update_job)
        if self.last_analysis_timestamp:
            elapsed_seconds = (datetime.now() - self.last_analysis_timestamp).total_seconds()
            if elapsed_seconds <= 10: color, status = "#008000", "Reciente"
            elif 11 <= elapsed_seconds <= 60: color, status = "#FFA500", "Moderado"
            else: color, status = "#FF0000", "Antiguo"
            if elapsed_seconds < 60: time_str = f"{int(elapsed_seconds)}s"
            elif elapsed_seconds < 3600: time_str = f"{int(elapsed_seconds//60)}m {int(elapsed_seconds%60)}s"
            else: time_str = f"{int(elapsed_seconds//3600)}h {int((elapsed_seconds%3600)//60)}m"
            self.timer_label_var.set(f"Último análisis: {time_str} ({status})")
            if hasattr(self, 'timer_label') and self.timer_label.winfo_exists(): self.timer_label.config(foreground=color)
        else:
            self.timer_label_var.set("Último análisis: N/A")
            if hasattr(self, 'timer_label') and self.timer_label.winfo_exists(): self.timer_label.config(foreground="#333333")
        self.timer_update_job = self.root.after(1000, self.update_timer_display)

    def add_ignore_item(self):
        item = self.ignore_entry.get().strip()
        if item:
            if item not in self.ignored_items:
                self.ignored_items.add(item)
                self.ignored_listbox.insert(tk.END, item); self.ignored_listbox.see(tk.END)
            self.ignore_entry.delete(0, tk.END)
            if self.persist_ignored_items_var.get(): self.save_config()

    def browse_file_to_ignore(self):
        fp = filedialog.askopenfilename(title="Seleccionar archivo a ignorar")
        if fp: self.ignore_entry.delete(0, tk.END); self.ignore_entry.insert(0, os.path.basename(fp)); self.add_ignore_item()

    def browse_folder_to_ignore(self):
        fp = filedialog.askdirectory(title="Seleccionar carpeta a ignorar")
        if fp: self.ignore_entry.delete(0, tk.END); self.ignore_entry.insert(0, os.path.basename(fp) + "/"); self.add_ignore_item()

    def remove_ignore_items(self):
        sel = self.ignored_listbox.curselection()
        if sel:
            items_to_rm = [self.ignored_listbox.get(i) for i in sel]
            for i in sorted(sel, reverse=True): self.ignored_listbox.delete(i)
            for item in items_to_rm: self.ignored_items.discard(item)
            if self.persist_ignored_items_var.get(): self.save_config()

    def clear_ignore_list(self):
        if messagebox.askyesno("Confirmar", "¿Limpiar toda la lista de elementos ignorados?"):
            self.ignored_listbox.delete(0, tk.END); self.ignored_items.clear()
            if self.persist_ignored_items_var.get(): self.save_config()

    def save_config(self):
        if self.loading_config: return
        try:
            config = {"persist_selected_folder": self.persist_selected_folder_var.get(),
                      "persist_output_location": self.persist_output_location_var.get(),
                      "persist_ignored_items": self.persist_ignored_items_var.get(),
                      "include_subdirs": self.include_subdirs_var.get(),
                      "show_empty_files": self.show_empty_files_var.get(),
                      "add_line_numbers": self.add_line_numbers_var.get(),
                      "show_directory_first": self.show_directory_first_var.get()}
            if config["persist_selected_folder"]: config["last_selected_folder"] = self.selected_folder.get()
            if config["persist_output_location"]: config["last_output_location"] = self.output_location.get()
            if config["persist_ignored_items"]: config["ignored_items"] = list(self.ignored_items)
            with open(self.config_file, 'w', encoding='utf-8') as f: json.dump(config, f, indent=4)
        except Exception as e: print(f"Error al guardar configuración: {e}")

    def load_config(self):
        self.loading_config = True
        default_output = os.path.join(os.path.expanduser("~"), "Desktop")
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f: config = json.load(f)
                self.persist_selected_folder_var.set(config.get("persist_selected_folder", True))
                self.persist_output_location_var.set(config.get("persist_output_location", True))
                self.persist_ignored_items_var.set(config.get("persist_ignored_items", True))
                if self.persist_selected_folder_var.get(): self.selected_folder.set(config.get("last_selected_folder", ""))
                else: self.selected_folder.set("") 
                self.output_location.set(config.get("last_output_location", default_output) if self.persist_output_location_var.get() else default_output)
                if self.persist_ignored_items_var.get():
                    self.ignored_items.clear(); self.ignored_listbox.delete(0, tk.END)
                    for item in config.get("ignored_items", []):
                        if item not in self.ignored_items: self.ignored_items.add(item); self.ignored_listbox.insert(tk.END, item)
                else: 
                    self.ignored_items.clear(); self.ignored_listbox.delete(0, tk.END)
                self.include_subdirs_var.set(config.get("include_subdirs", True))
                self.show_empty_files_var.set(config.get("show_empty_files", False))
                self.add_line_numbers_var.set(config.get("add_line_numbers", False))
                self.show_directory_first_var.set(config.get("show_directory_first", True))
            else: 
                self.selected_folder.set("")
                self.output_location.set(default_output)
                self.ignored_items.clear(); self.ignored_listbox.delete(0, tk.END)
        except Exception as e: 
            print(f"Error al cargar configuración: {e}")
            self.selected_folder.set("")
            self.output_location.set(default_output)
            self.ignored_items.clear(); self.ignored_listbox.delete(0, tk.END)
        finally: self.loading_config = False

    def browse_folder(self):
        f = filedialog.askdirectory(title="Seleccionar carpeta para analizar")
        if f: self.selected_folder.set(f)

    def browse_output(self):
        f = filedialog.askdirectory(title="Seleccionar carpeta para guardar el resultado")
        if f: self.output_location.set(f)

    def start_analysis(self):
        if not self.selected_folder.get(): 
            self.show_notification("Seleccione una carpeta para analizar.", msg_type="error")
            return
        if not os.path.isdir(self.selected_folder.get()): 
            self.show_notification("Ruta de carpeta a analizar inválida.", msg_type="error")
            return
        
        self.analyze_btn.config(state='disabled'); self.cancel_btn.config(state='normal')
        self.save_btn.config(state='disabled'); self.copy_btn.config(state='disabled')
        self.cancel_flag = False; self.analysis_result = ""
        self.last_analysis_timestamp = datetime.now(); self.update_timer_display()
        threading.Thread(target=self.analyze_folder, daemon=True).start()

    def cancel_analysis(self):
        self.cancel_flag = True; self.update_progress("Cancelando análisis...", self.progress_var.get())

    def analyze_folder(self):
        try:
            folder_path = self.selected_folder.get()
            self.update_progress("Escaneando archivos...", 0) 
            files_to_analyze = self.get_files_list(folder_path)

            if self.cancel_flag: self.reset_ui_after_analysis("Análisis cancelado (escaneo)"); return
            if not files_to_analyze:
                self.reset_ui_after_analysis("Sin archivos para analizar"); return

            self.update_progress(f"Preparando análisis de {len(files_to_analyze)} archivos...", 5)
            result_lines = [f"ANÁLISIS DE CARPETA\n{'='*80}",
                            f"Carpeta analizada: {folder_path}",
                            f"Fecha de análisis: {self.last_analysis_timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
                            f"Total de archivos analizados: {len(files_to_analyze)}",
                            f"Incluye subdirectorios: {'Sí' if self.include_subdirs_var.get() else 'No'}",
                            f"Mostrar archivos vacíos: {'Sí' if self.show_empty_files_var.get() else 'No'}",
                            f"Agregar números de línea: {'Sí' if self.add_line_numbers_var.get() else 'No'}",
                            f"Mostrar directorio primero: {'Sí' if self.show_directory_first_var.get() else 'No'}"]
            if self.ignored_items:
                result_lines.extend(["", "ELEMENTOS IGNORADOS", "-"*40])
                result_lines.extend([f"  • {item}" for item in sorted(list(self.ignored_items))])
            result_lines.append("\n" + "=" * 80)
            
            base_prog_content = 5
            if self.show_directory_first_var.get():
                result_lines.extend(["\nDIRECTORIO DE ARCHIVOS", "="*80])
                for idx, fp_list_item in enumerate(files_to_analyze):
                    if self.cancel_flag: break
                    self.update_progress(f"Listando: {os.path.basename(fp_list_item)}", 5 + (idx/len(files_to_analyze))*15)
                    result_lines.append(f"• {os.path.relpath(fp_list_item, os.path.dirname(folder_path))}")
                result_lines.extend(["\n" + "="*80, "CONTENIDO DE ARCHIVOS", "="*80])
                base_prog_content = 20
            
            if self.cancel_flag: self.reset_ui_after_analysis("Análisis cancelado (directorio)"); return

            for i, file_path_content in enumerate(files_to_analyze):
                if self.cancel_flag: break
                prog = base_prog_content + (i/len(files_to_analyze))*(95-base_prog_content)
                self.update_progress(f"Procesando: {os.path.basename(file_path_content)}", prog)
                self.analyze_file_to_result(result_lines, file_path_content, folder_path)
            
            if not self.cancel_flag:
                result_lines.append(f"\n{'='*80}\nFIN DEL ANÁLISIS\nGenerado el: {self.last_analysis_timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n{'='*80}")
                self.analysis_result = "\n".join(result_lines)
                self.update_progress("¡Análisis completado!", 100)
                self.root.after(0, lambda: [self.save_btn.config(state='normal'), self.copy_btn.config(state='normal')])
                self.root.after(100, lambda: self.show_notification("Análisis finalizado con éxito.", msg_type="success"))
            else: 
                self.update_progress("Análisis cancelado durante el procesamiento.", self.progress_var.get())
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error Crítico", f"Ocurrió un error durante el análisis:\n{e}"))
            self.update_progress(f"Error: {e}", self.progress_var.get())
        finally: 
            self.reset_ui_after_analysis()

    def get_files_list(self, folder_path):
        files = []
        deep_ignored_folder_names = {item.rstrip('/') for item in self.ignored_items if item.endswith('/') and '/' not in item.rstrip('/')}
        ignored_file_names = {item for item in self.ignored_items if not item.endswith('/') and '/' not in item}
        relative_ignored_paths = {os.path.normpath(item) for item in self.ignored_items if '/' in item}
        if self.include_subdirs_var.get():
            for root, dirs, fnames in os.walk(folder_path, topdown=True):
                current_rel_root = os.path.relpath(root, folder_path); current_rel_root = "" if current_rel_root == '.' else current_rel_root
                dirs_to_remove = []
                for d_name in dirs:
                    if d_name in deep_ignored_folder_names or os.path.normpath(os.path.join(current_rel_root, d_name + "/")) in relative_ignored_paths:
                        dirs_to_remove.append(d_name)
                dirs[:] = [d for d in dirs if d not in dirs_to_remove]
                for filename in fnames:
                    if filename in ignored_file_names or os.path.normpath(os.path.join(current_rel_root, filename)) in relative_ignored_paths: continue
                    if self.is_supported_file(filename): files.append(os.path.join(root, filename))
        else: 
            for item_name in os.listdir(folder_path):
                item_abs_path = os.path.join(folder_path, item_name)
                if os.path.isdir(item_abs_path):
                    if item_name in deep_ignored_folder_names or os.path.normpath(item_name + "/") in relative_ignored_paths: continue
                elif os.path.isfile(item_abs_path):
                    if item_name in ignored_file_names or os.path.normpath(item_name) in relative_ignored_paths: continue
                    if self.is_supported_file(item_name): files.append(item_abs_path)
        return sorted(files)

    def is_supported_file(self, filename):
        return os.path.splitext(filename)[1].lower() in self.supported_extensions

    def analyze_file_to_result(self, result_lines, file_path, base_folder):
        try:
            rel_path = os.path.relpath(file_path, os.path.dirname(base_folder))
            filename = os.path.basename(file_path)
            result_lines.append(f"\n{'='*80}\nArchivo: {filename}\nRuta: {rel_path}\n{'-'*40}")
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f: content = f.read()
            if not content.strip() and not self.show_empty_files_var.get():
                result_lines.append("(Archivo vacío - omitido según configuración)"); return
            language = self.get_language_from_extension(os.path.splitext(filename)[1].lower())
            result_lines.append(f"Contenido ({language}):\n```{language}")
            if self.add_line_numbers_var.get():
                for i, line in enumerate(content.splitlines(), 1): result_lines.append(f"{i:4d}| {line}")
            else: result_lines.append(content)
            result_lines.append("```")
        except Exception as e: result_lines.append(f"(Error al leer o procesar el archivo '{os.path.basename(file_path)}': {e})")

    def get_language_from_extension(self, ext):
        lang_map = {'.py': 'python', '.js': 'javascript', '.jsx': 'jsx', '.ts': 'typescript', 
                    '.tsx': 'tsx', '.html': 'html', '.htm': 'html', '.css': 'css', '.scss': 'scss', 
                    '.sass': 'sass', '.json': 'json', '.xml': 'xml', '.yaml': 'yaml', '.yml': 'yaml',
                    '.md': 'markdown', '.txt': 'text', '.sql': 'sql', '.php': 'php', '.java': 'java',
                    '.c': 'c', '.cpp': 'cpp', '.h': 'c', '.cs': 'csharp', '.rb': 'ruby', '.go': 'go',
                    '.rs': 'rust', '.swift': 'swift', '.kt': 'kotlin', '.vue': 'vue', '.svelte': 'svelte',
                    '.sh': 'bash', '.bat': 'batch', '.ps1': 'powershell', '.dockerfile': 'dockerfile'}
        return lang_map.get(ext, 'text') 
    
    def save_analysis(self):
        if not self.analysis_result: 
            self.show_notification("No hay análisis para guardar.", msg_type="error")
            return
        try:
            folder_name_base = os.path.basename(self.selected_folder.get()) if self.selected_folder.get() else "analisis"
            timestamp = (self.last_analysis_timestamp or datetime.now()).strftime("%Y%m%d_%H%M%S")
            suggested_name = f"{folder_name_base}_{timestamp}.txt"
            output_dir = self.output_location.get()
            if not (output_dir and os.path.isdir(output_dir)): 
                output_dir = os.path.join(os.path.expanduser("~"), "Desktop")
            
            file_path_save = filedialog.asksaveasfilename(
                title="Guardar Análisis Como...", initialdir=output_dir, initialfile=suggested_name, 
                defaultextension=".txt", filetypes=[("Archivos de Texto", "*.txt"), ("Todos los Archivos", "*.*")])
            
            if file_path_save:
                with open(file_path_save, 'w', encoding='utf-8') as f: f.write(self.analysis_result)
                self.show_notification(f"Análisis guardado en:\n{os.path.basename(file_path_save)}", msg_type="success", duration=4000)
        except Exception as e: 
            messagebox.showerror("Error al Guardar", f"No se pudo guardar el archivo:\n{e}")

    def copy_to_clipboard(self):
        if not self.analysis_result: 
            self.show_notification("No hay análisis para copiar.", msg_type="error")
            return
        try: 
            pyperclip.copy(self.analysis_result)
            self.show_notification("Análisis copiado al portapapeles.", msg_type="success")
        except pyperclip.PyperclipException as e:
             messagebox.showerror("Error de Portapapeles", f"No se pudo copiar al portapapeles:\n{e}\nAsegúrese de tener un gestor de portapapeles (ej. xclip o xsel en Linux).")
        except Exception as e: 
            messagebox.showerror("Error al Copiar", f"Ocurrió un error desconocido al copiar:\n{e}")

    def update_progress(self, text, value):
        def _update_gui():
            if hasattr(self, 'progress_label') and self.progress_label.winfo_exists(): self.progress_label.config(text=text)
            if hasattr(self, 'progress_bar') and self.progress_bar.winfo_exists(): self.progress_var.set(value)
        if hasattr(self, 'root') and self.root.winfo_exists(): self.root.after(0, _update_gui)

    def reset_ui_after_analysis(self, explicit_message=None):
        def _reset_gui_elements():
            if not (hasattr(self, 'root') and self.root.winfo_exists()): return
            if hasattr(self,'analyze_btn') and self.analyze_btn.winfo_exists(): self.analyze_btn.config(state='normal')
            if hasattr(self,'cancel_btn') and self.cancel_btn.winfo_exists(): self.cancel_btn.config(state='disabled')
            final_message_to_display = "Listo para una nueva acción."
            if explicit_message: final_message_to_display = explicit_message
            elif self.analysis_result and not self.cancel_flag: final_message_to_display = "Análisis completado. " + final_message_to_display
            elif self.cancel_flag: pass 
            if hasattr(self, 'progress_label') and self.progress_label.winfo_exists(): self.progress_label.config(text=final_message_to_display)
            if self.cancel_flag and self.progress_var.get() < 5:
                 if hasattr(self, 'progress_bar') and self.progress_bar.winfo_exists(): self.progress_var.set(0)
        if hasattr(self, 'root') and self.root.winfo_exists(): self.root.after(0, _reset_gui_elements)

def main():
    try: 
        import pyperclip
    except ImportError:
        class MockPyperclip:
            class PyperclipException(Exception): pass
            @staticmethod
            def copy(text): print("--- SIMULATED COPY ---\n",text,"\n--- END SIMULATED COPY ---"); raise MockPyperclip.PyperclipException("pyperclip no instalado.")
            @staticmethod
            def paste(): return ""
        import sys; sys.modules['pyperclip'] = MockPyperclip
        print("Advertencia: El módulo 'pyperclip' no está instalado.")
        print("La funcionalidad de copiar al portapapeles será simulada en la consola.")
        print("Para la funcionalidad completa, instale pyperclip: pip install pyperclip")

    root = tk.Tk()
    app = FolderAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()