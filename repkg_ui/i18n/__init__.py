"""
RePKG UI - Internationalization
==============================

Multi-language support system for the application.
"""

import json
import os
from ..constants import DEFAULT_LANGUAGE, AVAILABLE_LANGUAGES


class LanguageManager:
    """Manages application language and translations."""
    
    def __init__(self):
        """Initialize language manager."""
        self.current_language = DEFAULT_LANGUAGE
        self.translations = {}
        self.load_all_languages()
    
    def load_all_languages(self):
        """Load all available language files."""
        for lang in AVAILABLE_LANGUAGES:
            self.load_language(lang)
    
    def load_language(self, language_code):
        """Load a specific language file."""
        try:
            lang_file = os.path.join(os.path.dirname(__file__), f"{language_code}.json")
            if os.path.exists(lang_file):
                with open(lang_file, 'r', encoding='utf-8') as f:
                    self.translations[language_code] = json.load(f)
            else:
                # Fallback to English if file doesn't exist
                if language_code != 'en':
                    self.load_language('en')
        except Exception:
            # Silent fail, use English fallback
            if language_code != 'en':
                self.load_language('en')
    
    def set_language(self, language_code):
        """Set the current language."""
        if language_code in AVAILABLE_LANGUAGES:
            self.current_language = language_code
            if language_code not in self.translations:
                self.load_language(language_code)
    
    def get_text(self, key, **kwargs):
        """Get translated text for a key with optional formatting."""
        # Try current language first
        text = self._get_nested_value(self.translations.get(self.current_language, {}), key)
        
        # Fallback to English if not found
        if text is None and self.current_language != 'en':
            text = self._get_nested_value(self.translations.get('en', {}), key)
        
        # Final fallback to the key itself
        if text is None:
            text = key
        
        # Format with provided kwargs
        try:
            return text.format(**kwargs)
        except:
            return text
    
    def _get_nested_value(self, data, key):
        """Get value from nested dictionary using dot notation."""
        keys = key.split('.')
        value = data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return None
        
        return value
    
    def get_available_languages(self):
        """Get list of available languages with their display names."""
        return {
            'en': 'English',
            'vi': 'Tiếng Việt'
        }


# Global language manager instance
language_manager = LanguageManager()

# Convenience function for getting translations
def _(key, **kwargs):
    """Shorthand function for getting translated text."""
    return language_manager.get_text(key, **kwargs)
