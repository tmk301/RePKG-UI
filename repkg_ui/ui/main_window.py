"""
RePKG UI - Main Window
=====================

Main application window with all UI components and event handlers.
"""

import ttkbootstrap as ttk
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
        
        # Right side buttons
        right_frame = ttk.Frame(self.window)
        right_frame.grid(row=0, column=2, pady=8, padx=(0, 15), sticky="e")
        
        # Language toggle button
        current_lang = language_manager.current_language
        lang_icon = "🇺🇸" if current_lang == "en" else "🇻🇳"
        self.btn_language = ttk.Button(right_frame, text=lang_icon, 
                                      command=self._toggle_language, 
                                      style="outline.TButton", width=4)
        self.btn_language.pack(side="left", padx=(0, 5))
        
        # Theme toggle button
        theme_icon = THEME_ICONS.get("light" if self.current_theme == "dark" else "dark", "🌙")
        self.btn_theme = ttk.Button(right_frame, text=theme_icon, 
                                   command=self._toggle_theme, 
                                   style="outline.TButton", width=4)
        self.btn_theme.pack(side="left", padx=(0, 5))
        
        self.btn_reset = ttk.Button(right_frame, text=translate("reset"), 
                                   command=self._reset_to_default, 
                                   style="warning.TButton", width=8)
        self.btn_reset.pack(side="left", padx=(0, 5))
        
        self.btn_about = ttk.Button(right_frame, text=translate("about"), 
                                   command=self._show_about, 
                                   style="info.TButton", width=8)
        self.btn_about.pack(side="left")
    
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

        self.btn_input_file = ttk.Button(self.input_buttons_frame, text=translate("file"), command=self._select_file,
                                         style="outline.TButton", width=10)
        self.btn_input_file.pack(side="top", pady=(0, 2))
        self.btn_input_folder = ttk.Button(self.input_buttons_frame, text=translate("folder"), command=self._select_folder,
                                           style="outline.TButton", width=10)
        self.btn_input_folder.pack(side="top")

        # Output row
        self.label_output = ttk.Label(self.window, text=translate("output"), anchor="w")
        self.label_output.grid(row=2, column=0, sticky="w", pady=8, padx=(10, 5))

        self.entry_output = ttk.Entry(self.window, width=50, textvariable=self.var_output)
        self.entry_output.grid(row=2, column=1, pady=8, sticky="ew", padx=(0, 10))

        self.btn_browse_output = ttk.Button(self.window, text=translate("browse"),
                                            command=self._select_output_folder,
                                            style="outline.TButton", width=10)
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
        
        self.btn_advanced = ttk.Button(center_frame, text=translate("show_advanced"),
                                      command=self._toggle_advanced, 
                                      style="info.TButton", width=25)
        self.btn_advanced.pack(side="left", padx=(0, 10))
        
        ttk.Button(center_frame, text=translate("run"), command=self._run_repkg,
                  style="success.TButton", width=20).pack(side="left")
    
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
            self.btn_advanced.config(text=translate("show_advanced"))
        else:
            self.advanced_frame.grid()
            self.btn_advanced.config(text=translate("hide_advanced"))
    
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
    
    def _show_about(self):
        """Show about dialog."""
        show_about_dialog(self.window)
    
    def _toggle_theme(self):
        """Toggle between light and dark themes."""
        # Switch theme
        new_theme = "light" if self.current_theme == "dark" else "dark"
        self.current_theme = new_theme
        
        # Save theme preference
        config_manager.set_theme(new_theme)
        
        # Update button icon
        new_icon = THEME_ICONS.get("light" if new_theme == "dark" else "dark", "🌙")
        self.btn_theme.config(text=new_icon)
        
        # Apply new theme
        theme_name = THEMES.get(new_theme, WINDOW_THEME)
        self.style.theme_use(theme_name)
        
        # Reconfigure custom styles for new theme
        configure_custom_styles(self.style, theme_name)
    
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
    
    def _toggle_language(self):
        """Toggle between available languages."""
        current_lang = language_manager.current_language
        new_lang = "vi" if current_lang == "en" else "en"
        
        # Update language manager
        language_manager.set_language(new_lang)
        
        # Save language preference
        config_manager.set_language(new_lang)
        
        # Update UI with new language
        self._update_ui_language()
    
    def _update_ui_language(self):
        """Update all UI text with current language."""
        # Update window title
        self.window.title(translate("app_title"))
        
        # Update language button icon
        current_lang = language_manager.current_language
        lang_icon = "🇺🇸" if current_lang == "en" else "🇻🇳"
        self.btn_language.config(text=lang_icon)
        
        # Update button texts
        self.btn_reset.config(text=translate("reset"))
        self.btn_about.config(text=translate("about"))
        self.btn_input_file.config(text=translate("file"))
        self.btn_input_folder.config(text=translate("folder"))
        self.btn_browse_output.config(text=translate("browse"))
        
        # Update advanced frame text
        self.advanced_frame.config(text=translate("advanced_options"))
        
        # Update advanced button text
        if self.advanced_frame.winfo_ismapped():
            self.btn_advanced.config(text=translate("hide_advanced"))
        else:
            self.btn_advanced.config(text=translate("show_advanced"))
        
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
    
    def run(self):
        """Start the application."""
        self.window.mainloop()
