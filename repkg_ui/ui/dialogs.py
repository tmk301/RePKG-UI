"""
RePKG UI - Dialog Windows
=========================

Contains all dialog windows including About dialog and confirmation dialogs.
"""

import ttkbootstrap as ttk
import webbrowser
from tkinter import messagebox
from ..constants import (APP_NAME, APP_AUTHOR, APP_REPO, ORIGINAL_REPO, 
                        ABOUT_WINDOW_GEOMETRY)


def show_about_dialog(parent):
    """
    Display the About dialog window with application information.
    
    Args:
        parent: Parent window
    """
    about_win = ttk.Toplevel(parent)
    about_win.title(f"About {APP_NAME}")
    about_win.geometry(ABOUT_WINDOW_GEOMETRY)
    about_win.resizable(False, False)
    
    # Main content frame
    content_frame = ttk.Frame(about_win)
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Title
    ttk.Label(content_frame, text=APP_NAME, 
             font=("TkDefaultFont", 14, "bold")).pack(pady=(0, 10))
    
    # Created by section
    ttk.Label(content_frame, text=f"Created by {APP_AUTHOR}:").pack()
    link_btn1 = ttk.Button(content_frame, text=APP_REPO, 
                          command=lambda: webbrowser.open(APP_REPO),
                          style="link.TButton")
    link_btn1.pack(pady=(2, 10))
    
    # Based on section  
    ttk.Label(content_frame, text="Based on RePKG by notscuffed:").pack()
    link_btn2 = ttk.Button(content_frame, text=ORIGINAL_REPO,
                          command=lambda: webbrowser.open(ORIGINAL_REPO),
                          style="link.TButton")
    link_btn2.pack(pady=(2, 15))
    
    # Close button
    ttk.Button(content_frame, text="Close", 
              command=about_win.destroy, 
              style="outline.TButton").pack()


def show_reset_confirmation():
    """
    Show confirmation dialog for reset operation.
    
    Returns:
        bool: True if user confirms reset, False otherwise
    """
    return messagebox.askyesno(
        "Reset Confirmation", 
        "Are you sure you want to reset all settings to default values?\n\n"
        "This action cannot be undone.",
        icon="warning"
    )


def show_missing_input_warning():
    """Show warning dialog for missing input."""
    messagebox.showwarning("Missing Input", "Please select an input file or folder.")


def show_completion_message():
    """Show completion message after command execution."""
    messagebox.showinfo("Done", "RePKG command has completed.")


def show_error_message(error_msg):
    """
    Show error message dialog.
    
    Args:
        error_msg (str): Error message to display
    """
    messagebox.showerror("Error", str(error_msg))
