"""
RePKG UI - Custom Styles
========================

Defines custom styles and themes for the application interface.
"""

import ttkbootstrap as ttk
from ..constants import LINK_COLOR, LINK_HOVER_COLOR, LINK_PRESSED_COLOR


def configure_custom_styles(style, theme_name="darkly"):
    """
    Configure custom styles for the application.
    
    Args:
        style: ttkbootstrap Style object
        theme_name: Current theme name for theme-aware styling
    """
    # Link button style for clickable links
    link_color = LINK_COLOR
    if theme_name in ["flatly", "cosmo", "litera", "minty", "lumen"]:  # Light themes
        link_color = "#0066CC"  # Darker blue for light themes
    
    style.configure("link.TButton", 
                   foreground=link_color,
                   borderwidth=0,
                   relief="flat")
    
    style.map("link.TButton",
             foreground=[("active", LINK_HOVER_COLOR), 
                        ("pressed", LINK_PRESSED_COLOR)])


def get_theme_colors(theme_name):
    """
    Get theme-specific colors for dynamic styling.
    
    Args:
        theme_name: Name of the current theme
        
    Returns:
        dict: Theme color configuration
    """
    if theme_name in ["darkly", "cyborg", "superhero", "solar", "vapor"]:
        return {
            "bg": "#2b3e50",
            "fg": "#ffffff",
            "accent": "#3498db",
            "is_dark": True
        }
    else:
        return {
            "bg": "#ffffff", 
            "fg": "#212529",
            "accent": "#007bff",
            "is_dark": False
        }
