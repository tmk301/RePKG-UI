"""
RePKG UI - Configuration Management
==================================

Handles all configuration file operations including loading, saving, and auto-save functionality.
"""

import configparser
import os
from ..constants import CONFIG_FILE, DEFAULT_CONFIG


class ConfigManager:
    """Manages application configuration with auto-save capabilities."""
    
    def __init__(self):
        """Initialize configuration manager and load existing config."""
        self.config = configparser.ConfigParser()
        self._after_id = None
        self._window = None
        self.load_config()
    
    def set_window(self, window):
        """Set the window reference for auto-save timer functionality."""
        self._window = window
    
    def load_config(self):
        """Load configuration from file or create with defaults."""
        if os.path.exists(CONFIG_FILE):
            self.config.read(CONFIG_FILE)
        else:
            self.config["Settings"] = DEFAULT_CONFIG
            self.save_config_immediately()
    
    def get_setting(self, key, default=None):
        """Get a specific setting value."""
        return self.config["Settings"].get(key, default or DEFAULT_CONFIG.get(key, ""))
    
    def get_bool_setting(self, key):
        """Get a boolean setting value."""
        return self.get_setting(key).lower() == "true"
    
    def get_theme(self):
        """Get the current theme setting."""
        return self.get_setting("theme", "dark")
    
    def get_language(self):
        """Get the current language setting."""
        return self.get_setting("language", "en")
    
    def set_theme(self, theme):
        """Set the theme setting and save immediately."""
        current_settings = dict(self.config["Settings"])
        current_settings["theme"] = theme
        self.update_config(current_settings)
        self.save_config_immediately()  # Save immediately for theme changes
    
    def set_language(self, language):
        """Set the language setting and save immediately."""
        current_settings = dict(self.config["Settings"])
        current_settings["language"] = language
        self.update_config(current_settings)
        self.save_config_immediately()  # Save immediately for language changes
    
    def save_config_immediately(self):
        """Save configuration to file immediately."""
        try:
            with open(CONFIG_FILE, "w") as f:
                self.config.write(f)
        except Exception:
            pass  # Silent fail for config save
    
    def update_config(self, settings_dict):
        """Update configuration with new settings and trigger auto-save."""
        try:
            self.config["Settings"] = settings_dict
            self._schedule_auto_save()
        except Exception:
            pass  # Silent fail for config update
    
    def _schedule_auto_save(self):
        """Schedule auto-save with delay to prevent excessive I/O."""
        if self._window is None:
            return
            
        # Cancel previous scheduled save
        if self._after_id:
            self._window.after_cancel(self._after_id)
        
        # Schedule new save after delay
        from ..constants import AUTO_SAVE_DELAY
        self._after_id = self._window.after(AUTO_SAVE_DELAY, self.save_config_immediately)
    
    def reset_to_defaults(self):
        """Reset all settings to default values."""
        self.config["Settings"] = DEFAULT_CONFIG.copy()
        self.save_config_immediately()


# Global configuration manager instance
config_manager = ConfigManager()
