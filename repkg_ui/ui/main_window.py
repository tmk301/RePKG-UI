"""
RePKG UI - Main Window
=====================

Main application window with all UI components and event handlers.
"""

import ttkbootstrap as ttk
import tkinter as tk
import os

from ..constants import (WINDOW_GEOMETRY, WINDOW_THEME, APP_TITLE, EXTRACT_OPTIONS, 
                        INFO_OPTIONS, SORT_OPTIONS, CONSOLE_OUTPUT_HEIGHT, THEMES, THEME_ICONS)
from ..core.config import config_manager
from ..core.file_utils import get_icon_path, select_pkg_file, select_input_folder, select_output_folder
from ..core.repkg_runner import repkg_runner
from ..i18n import language_manager
from ..i18n import _ as translate
from .styles import configure_custom_styles, get_theme_colors
from .dialogs import (show_about_dialog, show_reset_confirmation, show_missing_input_warning,
                     show_completion_message, show_error_message)


class MainWindow:
    """Main application window class."""
    
    def __init__(self):
        """Initialize the main window and all components."""
        # Initialize language manager with saved language
        saved_language = config_manager.get_language()
        language_manager.set_language(saved_language)
        
        # Get saved theme
        self.current_theme = config_manager.get_theme()
        theme_name = THEMES.get(self.current_theme, WINDOW_THEME)
        
        self.window = ttk.Window(themename=theme_name)
        self.window.title(translate("app_title"))
        self.window.geometry(WINDOW_GEOMETRY)
        
        # Set window icon
        self._set_window_icon()
        
        # Configure styles
        self.style = ttk.Style()
        configure_custom_styles(self.style, theme_name)
        
        # Set config manager window reference
        config_manager.set_window(self.window)
        
        # Initialize UI variables
        self._init_variables()
        
        # Create UI components
        self._create_ui_components()
        
        # Setup event bindings
        self._setup_event_bindings()
        
        # Initialize UI state
        self._update_ui()
    
    def _set_window_icon(self):
        """Set the window icon if available."""
        try:
            icon_path = get_icon_path()
            if os.path.exists(icon_path):
                self.window.iconbitmap(icon_path)
        except Exception:
            pass  # Silent fail if icon cannot be loaded
    
    def _init_variables(self):
        """Initialize all UI variables."""
        # Mode selection
        self.var_mode = ttk.StringVar(value=config_manager.get_setting("mode"))
        
        # Input/Output paths
        self.var_input = ttk.StringVar(value=config_manager.get_setting("input"))
        self.var_output = ttk.StringVar(value=config_manager.get_setting("output"))
        
        # Extract options
        self.var_tex = ttk.BooleanVar(value=config_manager.get_bool_setting("tex"))
        self.var_singledir = ttk.BooleanVar(value=config_manager.get_bool_setting("singledir"))
        self.var_usename = ttk.BooleanVar(value=config_manager.get_bool_setting("usename"))
        self.var_no_tex_convert = ttk.BooleanVar(value=config_manager.get_bool_setting("no_tex_convert"))
        self.var_overwrite = ttk.BooleanVar(value=config_manager.get_bool_setting("overwrite"))
        self.var_copyproject = ttk.BooleanVar(value=config_manager.get_bool_setting("copyproject"))
        self.var_exts_only = ttk.StringVar(value=config_manager.get_setting("exts_only"))
        self.var_exts_ignore = ttk.StringVar(value=config_manager.get_setting("exts_ignore"))
        
        # Info options
        self.var_sortby = ttk.StringVar(value=config_manager.get_setting("sortby"))
        self.var_sort = ttk.BooleanVar(value=config_manager.get_bool_setting("sort"))
        self.var_printentries = ttk.BooleanVar(value=config_manager.get_bool_setting("printentries"))
        self.var_info_tex = ttk.BooleanVar(value=config_manager.get_bool_setting("info_tex"))
        self.var_projectinfo = ttk.StringVar(value=config_manager.get_setting("projectinfo"))
        self.var_title_filter = ttk.StringVar(value=config_manager.get_setting("title_filter"))
        
        # General options
        self.var_log = ttk.BooleanVar(value=config_manager.get_bool_setting("log"))
    
    def _create_ui_components(self):
        """Create all UI components."""
        self._create_mode_selection()
        self._create_input_output_section()
        self._create_advanced_options()
        self._create_action_buttons()
        self._create_output_console()
    
    def _calculate_button_width(self, text, min_width=8, padding=3):
        """Calculate optimal button width based on text content."""
        # More accurate character width estimation for different languages
        # Vietnamese and English have different character densities
        current_lang = language_manager.current_language
        char_width = 0.8 if current_lang == "vi" else 0.7  # Vietnamese needs more space
        
        # Calculate width based on text length + padding
        text_width = len(text) * char_width + padding
        return max(min_width, int(text_width) + 1)  # +1 for safety margin
    
    def _create_mode_selection(self):
        """Create mode selection row."""
        # Mode label and combobox
        ttk.Label(self.window, text=translate("mode"), anchor="w").grid(
            row=0, column=0, sticky="w", pady=8, padx=(10, 5))
        
        # Translated mode values
        mode_values = [translate("extract_mode"), translate("info_mode")]
        self.combo_mode = ttk.Combobox(self.window, values=mode_values, 
                                       state="readonly", width=15)
        self.combo_mode.grid(row=0, column=1, sticky="w", pady=8)
        
        # Set initial value based on config
        current_mode = self.var_mode.get()
        if current_mode == "extract":
            self.combo_mode.set(translate("extract_mode"))
        else:
            self.combo_mode.set(translate("info_mode"))
        
        # Right side settings button
        right_frame = ttk.Frame(self.window)
        right_frame.grid(row=0, column=2, pady=8, padx=(0, 15), sticky="e")
        
        # Settings button
        self.btn_settings = ttk.Button(right_frame, text="⚙️", 
                                      command=self._show_settings_menu, 
                                      style="outline.TButton", width=4)
        self.btn_settings.pack(side="left")
        
        # Configure grid column weights
        self.window.grid_columnconfigure(1, weight=1)
    
    def _create_input_output_section(self):
        """Create input and output selection section."""
        # Input row
        ttk.Label(self.window, text=translate("input"), anchor="w").grid(
            row=1, column=0, sticky="w", pady=8, padx=(10, 5))

        self.entry_input = ttk.Entry(self.window, width=50, textvariable=self.var_input)
        self.entry_input.grid(row=1, column=1, pady=8, sticky="ew", padx=(0, 10))

        # Store frame and buttons as attributes so we can hide folder button in info mode
        self.input_buttons_frame = ttk.Frame(self.window)
        self.input_buttons_frame.grid(row=1, column=2, pady=8, padx=(0, 15))

        # Auto-size buttons based on text content
        file_text = translate("file")
        folder_text = translate("folder")
        browse_text = translate("browse")
        
        file_width = self._calculate_button_width(file_text, min_width=10)
        folder_width = self._calculate_button_width(folder_text, min_width=10)
        browse_width = self._calculate_button_width(browse_text, min_width=10)

        self.btn_input_file = ttk.Button(self.input_buttons_frame, text=file_text, command=self._select_file,
                                         style="outline.TButton", width=file_width)
        self.btn_input_file.pack(side="top", pady=(0, 2))
        self.btn_input_folder = ttk.Button(self.input_buttons_frame, text=folder_text, command=self._select_folder,
                                           style="outline.TButton", width=folder_width)
        self.btn_input_folder.pack(side="top")

        # Output row
        self.label_output = ttk.Label(self.window, text=translate("output"), anchor="w")
        self.label_output.grid(row=2, column=0, sticky="w", pady=8, padx=(10, 5))

        self.entry_output = ttk.Entry(self.window, width=50, textvariable=self.var_output)
        self.entry_output.grid(row=2, column=1, pady=8, sticky="ew", padx=(0, 10))

        self.btn_browse_output = ttk.Button(self.window, text=browse_text,
                                            command=self._select_output_folder,
                                            style="outline.TButton", width=browse_width)
        self.btn_browse_output.grid(row=2, column=2, pady=8, padx=(0, 15))
    
    def _create_advanced_options(self):
        """Create advanced options panel."""
        self.advanced_frame = ttk.Labelframe(self.window, text=translate("advanced_options"), padding=10)
        self.advanced_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=10, pady=(10, 0))
        self.advanced_frame.grid_remove()  # Initially hidden
        
        # Create advanced option widgets (will be populated dynamically)
        self._create_advanced_widgets()
    
    def _create_advanced_widgets(self):
        """Create widgets for advanced options."""
        # Extract mode entries
        self.entry_exts_only = ttk.Entry(self.advanced_frame, width=40, textvariable=self.var_exts_only)
        self.entry_exts_ignore = ttk.Entry(self.advanced_frame, width=40, textvariable=self.var_exts_ignore)
        
        # Info mode widgets - don't use translated values here, just create the widget
        self.combo_sortby = ttk.Combobox(self.advanced_frame, values=["name", "extension", "size"],
                                        state="readonly", width=20, textvariable=self.var_sortby)
        self.entry_projectinfo = ttk.Entry(self.advanced_frame, width=40, textvariable=self.var_projectinfo)
        self.entry_title_filter = ttk.Entry(self.advanced_frame, width=40, textvariable=self.var_title_filter)
    
    def _create_action_buttons(self):
        """Create action buttons section."""
        button_frame = ttk.Frame(self.window)
        button_frame.grid(row=4, column=0, columnspan=3, pady=20, padx=20)
        
        center_frame = ttk.Frame(button_frame)
        center_frame.pack()
        
        # Auto-size buttons based on text content
        show_advanced_text = translate("show_advanced")
        run_text = translate("run")
        
        advanced_width = self._calculate_button_width(show_advanced_text, min_width=25)
        run_width = self._calculate_button_width(run_text, min_width=20)
        
        self.btn_advanced = ttk.Button(center_frame, text=show_advanced_text,
                                      command=self._toggle_advanced, 
                                      style="info.TButton", width=advanced_width)
        self.btn_advanced.pack(side="left", padx=(0, 10))
        
        ttk.Button(center_frame, text=run_text, command=self._run_repkg,
                  style="success.TButton", width=run_width).pack(side="left")
    
    def _create_output_console(self):
        """Create output console section."""
        output_frame = ttk.Labelframe(self.window, text=translate("console_output"), padding=10)
        output_frame.grid(row=98, column=0, columnspan=3, sticky="nsew", pady=(10, 0))
        
        self.text_output = ttk.ScrolledText(output_frame, height=CONSOLE_OUTPUT_HEIGHT, wrap="word")
        self.text_output.pack(fill="both", expand=True)
        
        # Configure grid weights
        self.window.grid_rowconfigure(98, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
    
    def _setup_event_bindings(self):
        """Setup all event bindings for auto-save."""
        # Mode change
        self.combo_mode.bind("<<ComboboxSelected>>", self._on_mode_change)
        
        # Variable traces for auto-save
        for var in [self.var_mode, self.var_input, self.var_output, self.var_exts_only, 
                   self.var_exts_ignore, self.var_projectinfo, self.var_title_filter,
                   self.var_sortby]:
            var.trace_add("write", self._on_config_change)
        
        for var in [self.var_tex, self.var_singledir, self.var_usename, self.var_no_tex_convert,
                   self.var_overwrite, self.var_copyproject, self.var_sort, self.var_printentries,
                   self.var_info_tex, self.var_log]:
            var.trace_add("write", self._on_config_change)
        
        # Combobox events
        self.combo_sortby.bind("<<ComboboxSelected>>", self._on_sortby_change)
    
    def _on_mode_change(self, *args):
        """Handle mode change event."""
        # Convert displayed mode back to internal value
        displayed_mode = self.combo_mode.get()
        if displayed_mode == translate("extract_mode"):
            self.var_mode.set("extract")
        elif displayed_mode == translate("info_mode"):
            self.var_mode.set("info")
        
        self._update_ui()
        self._on_config_change()
    
    def _on_sortby_change(self, *args):
        """Handle sortby combobox change event."""
        # Convert displayed sort option back to internal value
        displayed_sort = self.combo_sortby.get()
        if displayed_sort == translate("sort_options.name"):
            self.var_sortby.set("name")
        elif displayed_sort == translate("sort_options.extension"):
            self.var_sortby.set("extension")
        elif displayed_sort == translate("sort_options.size"):
            self.var_sortby.set("size")
        
        self._on_config_change()
    
    def _on_config_change(self, *args):
        """Handle configuration change for auto-save."""
        settings = {
            "mode": self.var_mode.get(),
            "input": self.var_input.get().strip(),
            "output": self.var_output.get().strip(),
            "theme": self.current_theme,
            "language": language_manager.current_language,  # Include language in auto-save
            "log": str(self.var_log.get()).lower(),
            "tex": str(self.var_tex.get()).lower(),
            "singledir": str(self.var_singledir.get()).lower(),
            "usename": str(self.var_usename.get()).lower(),
            "no_tex_convert": str(self.var_no_tex_convert.get()).lower(),
            "overwrite": str(self.var_overwrite.get()).lower(),
            "copyproject": str(self.var_copyproject.get()).lower(),
            "exts_only": self.var_exts_only.get().strip(),
            "exts_ignore": self.var_exts_ignore.get().strip(),
            "sortby": self.var_sortby.get(),
            "sort": str(self.var_sort.get()).lower(),
            "printentries": str(self.var_printentries.get()).lower(),
            "info_tex": str(self.var_info_tex.get()).lower(),
            "projectinfo": self.var_projectinfo.get().strip(),
            "title_filter": str(self.var_title_filter.get()).strip()
        }
        config_manager.update_config(settings)
    
    def _update_ui(self):
        """Update UI based on current mode."""
        mode = self.var_mode.get()
        
        # Show/hide output controls & folder selection depending on mode
        if mode == "extract":
            # Re-show output widgets if they were hidden
            self.label_output.grid()
            self.entry_output.grid()
            self.btn_browse_output.grid()
            # Show folder button
            if hasattr(self, 'btn_input_folder'):
                self.btn_input_folder.pack(side="top")
            # Ensure advanced frame sits below output
            try:
                self.advanced_frame.grid_configure(row=3)
            except Exception:
                pass
        else:  # info mode
            # Hide output widgets entirely instead of disabling
            self.label_output.grid_remove()
            self.entry_output.grid_remove()
            self.btn_browse_output.grid_remove()
            # Hide folder selection button (only allow file picking)
            if hasattr(self, 'btn_input_folder'):
                self.btn_input_folder.pack_forget()
            # Move advanced frame up to fill gap
            try:
                self.advanced_frame.grid_configure(row=2)
            except Exception:
                pass
        
        # Clear existing advanced options
        for widget in self.advanced_frame.winfo_children():
            widget.grid_remove()
        
        row = 0
        
        if mode == "extract":
            self._create_extract_options(row)
        elif mode == "info":
            self._create_info_options(row)
    
    def _create_extract_options(self, start_row):
        """Create extract mode advanced options."""
        row = start_row
        
        # Extension filtering
        ttk.Label(self.advanced_frame, 
                 text=translate("labels.exts_only")).grid(
                 row=row, column=0, sticky="w", pady=5)
        self.entry_exts_only.grid(row=row, column=1, pady=5)
        row += 1
        
        ttk.Label(self.advanced_frame,
                 text=translate("labels.exts_ignore")).grid(
                 row=row, column=0, sticky="w", pady=5)
        self.entry_exts_ignore.grid(row=row, column=1, pady=5)
        row += 1
        
        # Extract options checkboxes
        for var_name, _ in EXTRACT_OPTIONS:
            var = getattr(self, f"var_{var_name}")
            ttk.Checkbutton(self.advanced_frame, text=translate(f"extract_options.{var_name}"), variable=var).grid(
                row=row, column=0, sticky="w", pady=3)
            row += 1
        
        # Log option
        ttk.Checkbutton(self.advanced_frame, text=translate("labels.save_log"), 
                       variable=self.var_log).grid(row=row, column=0, sticky="w", pady=8)
    
    def _create_info_options(self, start_row):
        """Create info mode advanced options."""
        row = start_row
        
        # Sort by
        ttk.Label(self.advanced_frame, text=translate("labels.sort_by")).grid(row=row, column=0, sticky="w", pady=5)
        # Update sort options with translated values
        sort_values = [translate(f"sort_options.{opt}") for opt in ["name", "extension", "size"]]
        self.combo_sortby.config(values=sort_values)
        # Set current value based on saved setting
        current_sort = self.var_sortby.get()
        if current_sort in ["name", "extension", "size"]:
            self.combo_sortby.set(translate(f"sort_options.{current_sort}"))
        self.combo_sortby.grid(row=row, column=1, sticky="w", pady=5)
        row += 1
        
        # Info options checkboxes
        for var_name, _ in INFO_OPTIONS:
            var = getattr(self, f"var_{var_name}")
            ttk.Checkbutton(self.advanced_frame, text=translate(f"info_options.{var_name}"), variable=var).grid(
                row=row, column=0, sticky="w", pady=3)
            row += 1
        
        # Project info entry
        ttk.Label(self.advanced_frame,
                 text=translate("labels.project_info")).grid(
                 row=row, column=0, sticky="w", pady=5)
        self.entry_projectinfo.grid(row=row, column=1, pady=5)
        row += 1
        
        # Title filter entry
        ttk.Label(self.advanced_frame, text=translate("labels.title_filter")).grid(row=row, column=0, sticky="w", pady=5)
        self.entry_title_filter.grid(row=row, column=1, pady=5)
        row += 1
        
        # Log option
        ttk.Checkbutton(self.advanced_frame, text=translate("labels.save_log"), 
                       variable=self.var_log).grid(row=row, column=0, sticky="w", pady=8)
    
    def _toggle_advanced(self):
        """Toggle advanced options visibility."""
        if self.advanced_frame.winfo_ismapped():
            self.advanced_frame.grid_remove()
            text = translate("show_advanced")
        else:
            self.advanced_frame.grid()
            text = translate("hide_advanced")
        
        # Update button with auto-sizing
        width = self._calculate_button_width(text, min_width=25)
        self.btn_advanced.config(text=text, width=width)
    
    def _select_file(self):
        """Handle file selection."""
        path = select_pkg_file()
        if path:
            self.var_input.set(path)
    
    def _select_folder(self):
        """Handle folder selection."""
        path = select_input_folder()
        if path:
            self.var_input.set(path)
    
    def _select_output_folder(self):
        """Handle output folder selection."""
        path = select_output_folder()
        if path:
            self.var_output.set(path)
    
    def _reset_to_default(self):
        """Reset all settings to default with confirmation."""
        if show_reset_confirmation():
            config_manager.reset_to_defaults()
            self._reload_from_config()
            self._update_ui()
    
    def _reload_from_config(self):
        """Reload all variables from configuration."""
        self.var_mode.set(config_manager.get_setting("mode"))
        self.var_input.set(config_manager.get_setting("input"))
        self.var_output.set(config_manager.get_setting("output"))
        
        # Reload theme
        self.current_theme = config_manager.get_theme()
        theme_icon = THEME_ICONS.get("light" if self.current_theme == "dark" else "dark", "🌙")
        self.btn_theme.config(text=theme_icon)
        
        self.var_tex.set(config_manager.get_bool_setting("tex"))
        self.var_singledir.set(config_manager.get_bool_setting("singledir"))
        self.var_usename.set(config_manager.get_bool_setting("usename"))
        self.var_no_tex_convert.set(config_manager.get_bool_setting("no_tex_convert"))
        self.var_overwrite.set(config_manager.get_bool_setting("overwrite"))
        self.var_copyproject.set(config_manager.get_bool_setting("copyproject"))
        self.var_exts_only.set(config_manager.get_setting("exts_only"))
        self.var_exts_ignore.set(config_manager.get_setting("exts_ignore"))
        self.var_sortby.set(config_manager.get_setting("sortby"))
        self.var_sort.set(config_manager.get_bool_setting("sort"))
        self.var_printentries.set(config_manager.get_bool_setting("printentries"))
        self.var_info_tex.set(config_manager.get_bool_setting("info_tex"))
        self.var_projectinfo.set(config_manager.get_setting("projectinfo"))
        self.var_title_filter.set(config_manager.get_setting("title_filter"))
        self.var_log.set(config_manager.get_bool_setting("log"))
    
    def _show_settings_menu(self):
        """Show settings dialog."""
        self._show_settings_dialog()
    
    def _show_about(self):
        """Show about dialog."""
        show_about_dialog(self.window)
    
    def _show_settings_dialog(self):
        """Show settings popup dialog."""
        # Create popup dialog (Toplevel without window manager decorations)
        popup = ttk.Toplevel(self.window)
        popup.overrideredirect(True)  # Remove window decorations
        popup.configure(background='gray20')
        
        # Main frame with padding
        main_frame = ttk.Frame(popup, padding=15, style="Card.TFrame")
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text=translate("settings"), 
                               font=("TkDefaultFont", 12, "bold"))
        title_label.pack(anchor="w", pady=(0, 10))
        
        # Language section
        lang_label = ttk.Label(main_frame, text=translate("language"), 
                              font=("TkDefaultFont", 10, "bold"))
        lang_label.pack(anchor="w", pady=(0, 5))
        
        # Language buttons
        lang_frame = ttk.Frame(main_frame)
        lang_frame.pack(fill="x", pady=(0, 10))
        
        current_lang = language_manager.current_language
        available_langs = language_manager.get_available_languages()
        
        for lang_code, lang_name in available_langs.items():
            style = "success.TButton" if lang_code == current_lang else "outline.TButton"
            width = self._calculate_button_width(lang_name, min_width=8)
            btn = ttk.Button(lang_frame, text=lang_name, style=style, width=width,
                           command=lambda code=lang_code: self._apply_setting_change(popup, lambda: self._change_language(code)))
            btn.pack(side="left", padx=(0, 8))
        
        # Theme section
        theme_label = ttk.Label(main_frame, text=translate("theme"), 
                               font=("TkDefaultFont", 10, "bold"))
        theme_label.pack(anchor="w", pady=(0, 5))
        
        # Theme buttons
        theme_frame = ttk.Frame(main_frame)
        theme_frame.pack(fill="x", pady=(0, 10))
        
        theme_options = [("dark", translate("dark_theme")), ("light", translate("light_theme"))]
        for theme_code, theme_name in theme_options:
            style = "success.TButton" if theme_code == self.current_theme else "outline.TButton"
            width = self._calculate_button_width(theme_name, min_width=8)
            btn = ttk.Button(theme_frame, text=theme_name, style=style, width=width,
                           command=lambda code=theme_code: self._apply_setting_change(popup, lambda: self._change_theme(code)))
            btn.pack(side="left", padx=(0, 8))
        
        # Action buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill="x", pady=(5, 0))
        
        # Reset button
        reset_text = translate("reset")
        reset_width = self._calculate_button_width(reset_text, min_width=8)
        reset_btn = ttk.Button(action_frame, text=reset_text, 
                              style="warning.TButton", width=reset_width,
                              command=lambda: self._apply_setting_change(popup, self._reset_to_default))
        reset_btn.pack(side="left", padx=(0, 8))
        
        # About button  
        about_text = translate("about")
        about_width = self._calculate_button_width(about_text, min_width=8)
        about_btn = ttk.Button(action_frame, text=about_text, 
                              style="info.TButton", width=about_width,
                              command=self._show_about)
        about_btn.pack(side="left", padx=(0, 8))
        
        # Close button
        close_btn = ttk.Button(action_frame, text="✕", 
                              style="secondary.TButton", width=3,
                              command=popup.destroy)
        close_btn.pack(side="right")
        
        # Position popup at center of main window
        self._center_popup(popup)
        
        # Make popup modal but allow interaction with about dialog
        popup.transient(self.window)
        popup.focus_set()
        
        # Close popup when clicking outside
        self._setup_popup_close_handler(popup)
    
    def _apply_setting_change(self, popup, action):
        """Apply setting change and close popup."""
        action()
        popup.destroy()
    
    def _center_popup(self, popup):
        """Center popup on main window."""
        popup.update_idletasks()
        
        try:
            # Get main window position and size
            main_x = self.window.winfo_rootx()
            main_y = self.window.winfo_rooty()
            main_width = self.window.winfo_width()
            main_height = self.window.winfo_height()
            
            # Get popup size
            popup_width = popup.winfo_width()
            popup_height = popup.winfo_height()
            
            # Calculate center position
            popup_x = main_x + (main_width - popup_width) // 2
            popup_y = main_y + (main_height - popup_height) // 2
            
            popup.geometry(f"+{popup_x}+{popup_y}")
        except:
            # Fallback to screen center
            screen_width = popup.winfo_screenwidth()
            screen_height = popup.winfo_screenheight()
            popup_x = (screen_width - popup.winfo_width()) // 2
            popup_y = (screen_height - popup.winfo_height()) // 2
            popup.geometry(f"+{popup_x}+{popup_y}")
    
    def _setup_popup_close_handler(self, popup):
        """Setup handler to close popup when clicking outside."""
        def close_popup(event=None):
            try:
                # Check if click is outside popup
                x, y = popup.winfo_pointerx(), popup.winfo_pointery()
                popup_x1 = popup.winfo_rootx()
                popup_y1 = popup.winfo_rooty()
                popup_x2 = popup_x1 + popup.winfo_width()
                popup_y2 = popup_y1 + popup.winfo_height()
                
                if not (popup_x1 <= x <= popup_x2 and popup_y1 <= y <= popup_y2):
                    popup.destroy()
            except:
                pass
        
        # Bind click events (with small delay to avoid immediate close)
        self.window.after(100, lambda: self.window.bind("<Button-1>", close_popup, add=True))
    
    def _run_repkg(self):
        """Execute RePKG command."""
        mode = self.var_mode.get()
        input_path = self.var_input.get().strip()
        output_path = self.var_output.get().strip()
        
        # Validate input
        if not input_path:
            show_missing_input_warning()
            return
        
        # Prepare options
        extract_options = None
        info_options = None
        
        if mode == "extract":
            extract_options = {
                "tex": self.var_tex.get(),
                "singledir": self.var_singledir.get(),
                "usename": self.var_usename.get(),
                "no_tex_convert": self.var_no_tex_convert.get(),
                "overwrite": self.var_overwrite.get(),
                "copyproject": self.var_copyproject.get(),
                "exts_only": self.var_exts_only.get().strip(),
                "exts_ignore": self.var_exts_ignore.get().strip()
            }
        elif mode == "info":
            info_options = {
                "sortby": self.var_sortby.get(),
                "sort": self.var_sort.get(),
                "printentries": self.var_printentries.get(),
                "info_tex": self.var_info_tex.get(),
                "projectinfo": self.var_projectinfo.get().strip(),
                "title_filter": self.var_title_filter.get().strip()
            }
        
        # Build and execute command
        cmd = repkg_runner.build_command(mode, input_path, output_path, 
                                        extract_options, info_options)
        output, error, success = repkg_runner.execute_command(cmd, self.var_log.get())
        
        # Display results
        self.text_output.delete("1.0", "end")
        self.text_output.insert("end", output)
        if error:
            self.text_output.insert("end", "\n[stderr]\n" + error)
        
        if success:
            show_completion_message()
        else:
            show_error_message(error or "Command failed")
    
    def _update_ui_language(self):
        """Update all UI text with current language."""
        # Update window title
        self.window.title(translate("app_title"))
        
        # Update button texts with auto-sizing
        self._update_button_sizes()
        
        # Update advanced frame text
        self.advanced_frame.config(text=translate("advanced_options"))
        
        # Update mode combobox values
        mode_values = [translate("extract_mode"), translate("info_mode")]
        current_selection = self.combo_mode.get()
        self.combo_mode.config(values=mode_values)
        
        # Restore selection based on actual mode
        current_mode = self.var_mode.get()
        if current_mode == "extract":
            self.combo_mode.set(translate("extract_mode"))
        else:
            self.combo_mode.set(translate("info_mode"))
        
        # Re-create advanced options to update labels
        self._update_ui()
    
    def _change_language(self, language_code):
        """Change language via menu."""
        language_manager.set_language(language_code)
        config_manager.set_language(language_code)
        self._update_ui_language()
    
    def _change_theme(self, theme):
        """Change theme via menu."""
        self.current_theme = theme
        config_manager.set_theme(theme)
        
        # Apply new theme
        theme_name = THEMES.get(theme, WINDOW_THEME)
        self.style.theme_use(theme_name)
        
        # Reconfigure custom styles for new theme
        configure_custom_styles(self.style, theme_name)
    
    def _update_button_sizes(self):
        """Update all button sizes based on current language."""
        # Update input/output buttons
        file_text = translate("file")
        folder_text = translate("folder") 
        browse_text = translate("browse")
        
        file_width = self._calculate_button_width(file_text, min_width=10)
        folder_width = self._calculate_button_width(folder_text, min_width=10)
        browse_width = self._calculate_button_width(browse_text, min_width=10)
        
        self.btn_input_file.config(text=file_text, width=file_width)
        self.btn_input_folder.config(text=folder_text, width=folder_width)
        self.btn_browse_output.config(text=browse_text, width=browse_width)
        
        # Update advanced button
        if self.advanced_frame.winfo_ismapped():
            advanced_text = translate("hide_advanced")
        else:
            advanced_text = translate("show_advanced")
        
        advanced_width = self._calculate_button_width(advanced_text, min_width=25)
        self.btn_advanced.config(text=advanced_text, width=advanced_width)
    
    def run(self):
        """Start the application."""
        self.window.mainloop()
