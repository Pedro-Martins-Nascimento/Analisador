import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import tkinter as tk
import sys
import time
import threading

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_SUPPORTED = True
except ImportError:
    DND_SUPPORTED = False
    print("AVISO: TkinterDnD2 não encontrado...")

AppBaseClass = TkinterDnD.Tk if DND_SUPPORTED else ctk.CTk

class FileUploaderApp(AppBaseClass):
    def __init__(self):
        super().__init__()

        self.title("Analisador de Moda")
        self.geometry("650x680")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.selected_files = []

        # --- Cores ---
        self.WINDOW_BG_COLOR = "#000000"
        self.CARD_FG_COLOR = "#121212"
        self.UNIFIED_AREA_FG_COLOR = "#1E1E1E"
        self.ITEM_FG_COLOR = "#282828"
        self.TEXT_COLOR_PRIMARY = "#E0E0E0"
        self.TEXT_COLOR_SECONDARY = "#A0A0A0"
        self.BUTTON_FG_COLOR = "#2A2A2A"
        self.BUTTON_HOVER_COLOR = "#3A3A3A"
        self.BUTTON_TEXT_COLOR = self.TEXT_COLOR_PRIMARY
        self.BUTTON_DISABLED_FG_COLOR = "#1C1C1C"
        self.BUTTON_DISABLED_TEXT_COLOR = "#555555"
        self.ADD_MORE_BUTTON_FG_COLOR = ("gray25", "gray20")
        self.ADD_MORE_BUTTON_HOVER_COLOR = ("gray35", "gray30")
        self.DELETE_X_TEXT_COLOR = ("#FF6B6B", "#FF8A80")
        self.DELETE_X_HOVER_COLOR = ("#FF8A80", "#FF6B6B")
        self.BORDER_COLOR = "#333333"
        self.MAIN_FRAME_BORDER_NORMAL = self.CARD_FG_COLOR
        self.MAIN_FRAME_BORDER_HOVER = "#555555"
        self.SCROLLBAR_FG_COLOR = self.UNIFIED_AREA_FG_COLOR
        self.SCROLLBAR_BUTTON_COLOR = self.TEXT_COLOR_SECONDARY
        self.SCROLLBAR_BUTTON_HOVER_COLOR = self.TEXT_COLOR_PRIMARY
        self.PROCESSING_WINDOW_FG_COLOR = self.CARD_FG_COLOR


        if isinstance(self, TkinterDnD.Tk) or isinstance(self, tk.Tk):
            self.configure(bg=self.WINDOW_BG_COLOR)
        elif isinstance(self, ctk.CTk):
             self.configure(fg_color=self.WINDOW_BG_COLOR)

        self._create_widgets()
        self.update_upload_button_state()
        self.after(50, self.update_unified_area)

        if DND_SUPPORTED:
            self.main_frame.drop_target_register(DND_FILES)
            self.main_frame.dnd_bind('<<Drop>>', self.handle_drop_event)
            self.main_frame.dnd_bind('<<DragEnter>>', self.handle_drag_enter_main)
            self.main_frame.dnd_bind('<<DragLeave>>', self.handle_drag_leave_main)
        self.main_frame.bind("<Button-1>", self.handle_main_frame_click)
        self.processing_window = None

    def show_processing_window(self):
        if self.processing_window is None or not self.processing_window.winfo_exists():
            self.processing_window = ctk.CTkToplevel(self)
            self.processing_window.title("Processando"); main_x=self.winfo_x(); main_y=self.winfo_y(); main_width=self.winfo_width(); main_height=self.winfo_height(); win_width=300; win_height=150; x=main_x+(main_width-win_width)//2; y=main_y+(main_height-win_height)//2; self.processing_window.geometry(f"{win_width}x{win_height}+{x}+{y}")
            self.processing_window.resizable(False,False); self.processing_window.transient(self); self.processing_window.grab_set(); self.processing_window.protocol("WM_DELETE_WINDOW",lambda:None); self.processing_window.configure(fg_color=self.PROCESSING_WINDOW_FG_COLOR)
            ctk.CTkLabel(self.processing_window,text="Processando arquivos...",font=ctk.CTkFont(family="Segoe UI",size=16),text_color=self.TEXT_COLOR_PRIMARY).pack(pady=20,expand=True)
            self.progress_bar=ctk.CTkProgressBar(self.processing_window,mode="indeterminate",progress_color=self.TEXT_COLOR_SECONDARY); self.progress_bar.pack(pady=(0,20),padx=20,fill="x"); self.progress_bar.start()
        else: self.processing_window.lift()

    def hide_processing_window(self):
        if self.processing_window and self.processing_window.winfo_exists():
            if hasattr(self,'progress_bar') and self.progress_bar.winfo_exists(): self.progress_bar.stop()
            self.processing_window.destroy(); self.processing_window=None
            try: self.grab_release()
            except tk.TclError: pass

    def actual_processing_logic(self):
        """Simula o envio para API e processamento."""
        print("Iniciando simulação de processamento dos arquivos selecionados...")
        for file_path in self.selected_files:
            print(f" - Processando: {os.path.basename(file_path)}")
            # Aqui você colocaria sua lógica de chamada de API para cada arquivo
            time.sleep(0.5) # Simula processamento por arquivo
        
        print("Simulação de processamento de todos os arquivos concluída.")
        
        # Após o processamento, chame a função para esconder a janela e limpar
        self.after(0, self.on_processing_finished, "Sucesso!", f"{len(self.selected_files)} arquivo(s) processados.")


    def on_processing_finished(self, title, message, msg_type="info"):
        """Chamado após a conclusão do processamento para atualizar a UI."""
        self.hide_processing_window()
        
        if msg_type == "info":
            messagebox.showinfo(title, message)
        elif msg_type == "error":
            messagebox.showerror(title, message)
        elif msg_type == "warning":
            messagebox.showwarning(title, message)
        
        # --- Limpar a lista de arquivos após o processamento ---
        self.selected_files.clear()
        self.update_unified_area() # Atualiza a UI para mostrar o placeholder
        self.update_upload_button_state() # Desabilita o botão de upload


    def upload_files_action(self):
        if not self.selected_files:
            messagebox.showwarning("Nenhum Arquivo", "Por favor, selecione ou arraste arquivos para analisar.")
            return

        self.show_processing_window()
        processing_thread = threading.Thread(target=self.actual_processing_logic, daemon=True)
        processing_thread.start()

    # ... (handle_main_frame_click, handle_drag_*, handle_drop_event, _create_widgets, update_unified_area, select_files_dialog, remove_file, update_upload_button_state)
    # Nenhuma mudança necessária nessas outras funções para esta funcionalidade específica.
    # Vou incluir o corpo delas para completude, mas a lógica principal da mudança está acima.

    def handle_main_frame_click(self, event):
        clicked_widget = event.widget
        if isinstance(clicked_widget, ctk.CTkButton) or isinstance(clicked_widget, ctk.CTkScrollbar): return
        if hasattr(self, 'placeholder_content_frame_ref') and self.placeholder_content_frame_ref is not None:
            if clicked_widget == self.dd_text_main_ref or clicked_widget == self.dd_text_sub_ref: return
        if clicked_widget == self.main_frame or \
           clicked_widget == self.unified_files_area or \
           (hasattr(self.unified_files_area, "_canvas") and clicked_widget == self.unified_files_area._canvas) or \
           (hasattr(self, 'placeholder_content_frame_ref') and clicked_widget == self.placeholder_content_frame_ref):
            self.select_files_dialog(event)

    def handle_drag_enter_main(self, event):
        if hasattr(self, 'main_frame') and self.main_frame.winfo_exists():
            self.main_frame.configure(border_color=self.MAIN_FRAME_BORDER_HOVER, border_width=3)

    def handle_drag_leave_main(self, event):
        if hasattr(self, 'main_frame') and self.main_frame.winfo_exists():
            x_root, y_root = event.x_root, event.y_root; widget_under_mouse = self.winfo_containing(x_root, y_root)
            is_still_over_target = False; current_widget = widget_under_mouse
            while current_widget:
                if current_widget == self.main_frame: is_still_over_target = True; break
                try: current_widget = current_widget.master
                except AttributeError: current_widget = None
            if not is_still_over_target: self.main_frame.configure(border_color=self.MAIN_FRAME_BORDER_NORMAL, border_width=0)

    def handle_drop_event(self, event):
        if hasattr(self, 'main_frame') and self.main_frame.winfo_exists():
            self.main_frame.configure(border_color=self.MAIN_FRAME_BORDER_NORMAL, border_width=0)
        filepaths_str = event.data; parsed_filepaths = []
        if filepaths_str:
            try:
                filepath_candidates = self.tk.splitlist(filepaths_str)
                for fp_candidate in filepath_candidates:
                    fp_candidate = fp_candidate.strip()
                    if fp_candidate: parsed_filepaths.append(fp_candidate)
            except Exception as e:
                print(f"Erro com tk.splitlist (tentando fallback): {e}")
                if filepaths_str.startswith('{') and filepaths_str.endswith('}'): filepaths_str = filepaths_str[1:-1]
                parts = filepaths_str.replace("} {", "}###SPLIT###{").split("###SPLIT###")
                for part in parts:
                    clean_part = part.strip().strip('{}')
                    if ' ' in clean_part and not os.path.exists(clean_part): parsed_filepaths.extend(p for p in clean_part.split() if p)
                    elif clean_part: parsed_filepaths.append(clean_part)
        if parsed_filepaths:
            added_any = False
            for fp_raw in parsed_filepaths:
                normalized_fp = os.path.normpath(fp_raw)
                if normalized_fp not in self.selected_files and os.path.isfile(normalized_fp):
                    self.selected_files.append(normalized_fp); added_any = True
            if added_any: self.update_unified_area(); self.update_upload_button_state()

    def _create_widgets(self):
        self.main_frame = ctk.CTkFrame(
            self, fg_color=self.CARD_FG_COLOR, corner_radius=15,
            border_width=0, border_color=self.MAIN_FRAME_BORDER_NORMAL
        )
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        title_font = ctk.CTkFont(family="Segoe UI", size=26, weight="bold")
        title_label = ctk.CTkLabel(self.main_frame, text="Analisador de Moda", font=title_font, text_color=self.TEXT_COLOR_PRIMARY)
        title_label.pack(pady=(20, 15))
        self.upload_button = ctk.CTkButton(
            self.main_frame, text="Analisar Arquivos", font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            command=self.upload_files_action, height=45, corner_radius=10,
            fg_color=self.BUTTON_FG_COLOR, hover_color=self.BUTTON_HOVER_COLOR,
            text_color=self.BUTTON_TEXT_COLOR, border_color=self.BORDER_COLOR, border_width=1
        )
        self.unified_files_area = ctk.CTkScrollableFrame(
            self.main_frame, label_text="", fg_color=self.UNIFIED_AREA_FG_COLOR,
            border_color=self.BORDER_COLOR, border_width=2, corner_radius=10,
            scrollbar_fg_color=self.UNIFIED_AREA_FG_COLOR,
            scrollbar_button_color=self.SCROLLBAR_BUTTON_COLOR,
            scrollbar_button_hover_color=self.SCROLLBAR_BUTTON_HOVER_COLOR
        )
        self.unified_files_area.pack(fill="both", expand=True, padx=20, pady=(5, 0))
        self.upload_button.pack(side="bottom", fill="x", padx=20, pady=(10, 20))
        self.placeholder_font_main = ctk.CTkFont(family="Segoe UI", size=14)
        self.placeholder_font_sub = ctk.CTkFont(family="Segoe UI", size=12, slant="italic")
        self.item_font = ctk.CTkFont(family="Segoe UI", size=13)
        self.delete_x_font = ctk.CTkFont(family="Arial", size=16, weight="bold")
        self.add_more_font = ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        self.placeholder_content_frame_ref = None
        self.dd_text_main_ref = None
        self.dd_text_sub_ref = None

    def update_unified_area(self):
        for widget in self.unified_files_area.winfo_children(): widget.destroy()
        self.unified_files_area.update_idletasks()
        if not self.selected_files:
            self.placeholder_content_frame_ref = ctk.CTkFrame(self.unified_files_area, fg_color="transparent")
            self.placeholder_content_frame_ref.pack(expand=True, anchor="center", padx=10, pady=20)
            if DND_SUPPORTED:
                self.placeholder_content_frame_ref.drop_target_register(DND_FILES)
                self.placeholder_content_frame_ref.dnd_bind('<<Drop>>', self.handle_drop_event)
                self.placeholder_content_frame_ref.dnd_bind('<<DragEnter>>', self.handle_drag_enter_main)
                self.placeholder_content_frame_ref.dnd_bind('<<DragLeave>>', self.handle_drag_leave_main)
            self.placeholder_content_frame_ref.bind("<Button-1>", self.select_files_dialog)
            self.dd_text_main_ref = ctk.CTkLabel(
                self.placeholder_content_frame_ref, text="Arraste e solte seus arquivos de moda aqui\n(ou clique para selecionar)",
                font=self.placeholder_font_main, text_color=self.TEXT_COLOR_PRIMARY, justify="center"
            )
            self.dd_text_main_ref.pack(pady=(10,5))
            self.dd_text_main_ref.bind("<Button-1>", self.select_files_dialog)
            self.dd_text_sub_ref = ctk.CTkLabel(
                self.placeholder_content_frame_ref, text="Formatos suportados: imagens, PDFs, etc.",
                font=self.placeholder_font_sub, text_color=self.TEXT_COLOR_SECONDARY, cursor="hand2"
            )
            self.dd_text_sub_ref.pack(pady=(0,10))
            self.dd_text_sub_ref.bind("<Button-1>", self.select_files_dialog)
        else:
            self.placeholder_content_frame_ref = None; self.dd_text_main_ref = None; self.dd_text_sub_ref = None
            for filepath_in_list in self.selected_files:
                filename = os.path.basename(filepath_in_list)
                item_frame = ctk.CTkFrame(self.unified_files_area, fg_color=self.ITEM_FG_COLOR, corner_radius=8, border_width=1, border_color=self.BORDER_COLOR)
                item_frame.pack(fill="x", pady=(3,2), padx=5)
                file_label = ctk.CTkLabel(item_frame, text=filename, font=self.item_font, text_color=self.TEXT_COLOR_PRIMARY, anchor="w")
                file_label.pack(side="left", fill="x", expand=True, padx=(10,10), pady=5)
                delete_button = ctk.CTkButton(item_frame, text="✕", font=self.delete_x_font, command=lambda cfp=filepath_in_list: self.remove_file(cfp),
                                              width=30, height=30, fg_color="transparent", text_color=self.DELETE_X_TEXT_COLOR, hover_color=self.DELETE_X_HOVER_COLOR)
                delete_button.pack(side="right", padx=(0,5), pady=5)
            add_more_button = ctk.CTkButton(self.unified_files_area, text="+ Adicionar Mais", font=self.add_more_font, command=self.select_files_dialog,
                                            fg_color=self.ADD_MORE_BUTTON_FG_COLOR, hover_color=self.ADD_MORE_BUTTON_HOVER_COLOR, text_color=self.TEXT_COLOR_PRIMARY,
                                            height=35, border_width=1, border_color=self.BORDER_COLOR, corner_radius=8)
            add_more_button.pack(fill="x", pady=(10,5), padx=5)

    def select_files_dialog(self, event=None):
        filepaths_tuple = filedialog.askopenfilenames(title="Selecionar Arquivos para Análise",
                                                     filetypes=(("Todos os Arquivos Suportados", "*.jpg *.jpeg *.png *.pdf"),
                                                                ("Imagens", "*.jpg *.jpeg *.png"), ("Documentos PDF", "*.pdf"),
                                                                ("Todos os arquivos", "*.*")))
        if filepaths_tuple:
            added_any = False
            for fp_candidate in filepaths_tuple:
                normalized_fp = os.path.normpath(fp_candidate)
                if normalized_fp not in self.selected_files and os.path.isfile(normalized_fp):
                    self.selected_files.append(normalized_fp); added_any = True
            if added_any: self.update_unified_area(); self.update_upload_button_state()

    def remove_file(self, filepath_to_remove):
        normalized_filepath_to_remove = os.path.normpath(filepath_to_remove)
        if normalized_filepath_to_remove in self.selected_files:
            self.selected_files.remove(normalized_filepath_to_remove)
            self.update_unified_area(); self.update_upload_button_state()

    def update_upload_button_state(self):
        if hasattr(self, 'upload_button') and self.upload_button.winfo_exists():
            state = "normal" if self.selected_files else "disabled"
            fg = self.BUTTON_FG_COLOR if self.selected_files else self.BUTTON_DISABLED_FG_COLOR
            txt_color = self.BUTTON_TEXT_COLOR if self.selected_files else self.BUTTON_DISABLED_TEXT_COLOR
            self.upload_button.configure(state=state, fg_color=fg, text_color=txt_color)


if __name__ == "__main__":
    app = FileUploaderApp()
    if isinstance(app, TkinterDnD.Tk) or isinstance(app, tk.Tk) :
        app.configure(bg=app.WINDOW_BG_COLOR)
    elif isinstance(app, ctk.CTk):
        app.configure(fg_color=app.WINDOW_BG_COLOR)
    app.mainloop()