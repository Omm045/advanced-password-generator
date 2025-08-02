"""
Custom GUI Components for Password Generator
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Any

class CustomWidgets:
    """Custom widget implementations"""
    
    def __init__(self, parent):
        self.parent = parent
        
    def create_strength_meter(self, parent, width=200, height=20):
        """Create a custom strength meter widget"""
        canvas = tk.Canvas(parent, width=width, height=height, 
                          bg="#2a2a3e", highlightthickness=0)
        
        # Draw background
        canvas.create_rectangle(0, 0, width, height, fill="#2a2a3e", outline="#555")
        
        return canvas
        
    def update_strength_meter(self, canvas, strength_score):
        """Update strength meter display"""
        canvas.delete("strength_bar")
        
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        
        # Calculate bar width
        bar_width = (strength_score / 100) * width
        
        # Determine color based on strength
        if strength_score < 20:
            color = "#ff4444"  # Red
        elif strength_score < 40:
            color = "#ff8800"  # Orange  
        elif strength_score < 60:
            color = "#ffff00"  # Yellow
        elif strength_score < 80:
            color = "#88ff00"  # Light green
        else:
            color = "#00ff00"  # Green
            
        # Draw strength bar
        canvas.create_rectangle(0, 0, bar_width, height, 
                               fill=color, outline="", tags="strength_bar")
        
    def create_password_field(self, parent, show_toggle=True):
        """Create a password field with show/hide toggle"""
        frame = ttk.Frame(parent)
        
        password_var = tk.StringVar()
        show_var = tk.BooleanVar()
        
        entry = ttk.Entry(frame, textvariable=password_var, show="*")
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        if show_toggle:
            def toggle_visibility():
                if show_var.get():
                    entry.config(show="")
                else:
                    entry.config(show="*")
                    
            show_btn = ttk.Checkbutton(frame, text="👁", variable=show_var,
                                      command=toggle_visibility)
            show_btn.pack(side=tk.RIGHT, padx=(5, 0))
            
        return frame, password_var
        
    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=text, background="#ffffe0", 
                           relief=tk.SOLID, borderwidth=1, font=("Arial", 8))
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
                
            tooltip.after(3000, hide_tooltip)  # Hide after 3 seconds
            widget.tooltip = tooltip
            
        def hide_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                
        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)
        
    def create_animated_button(self, parent, text, command, **kwargs):
        """Create an animated button with hover effects"""
        default_bg = kwargs.get('bg', '#16213e')
        hover_bg = kwargs.get('hover_bg', '#00d4ff')
        
        button = tk.Button(parent, text=text, command=command,
                          bg=default_bg, fg='white', relief=tk.FLAT,
                          font=kwargs.get('font', ('Segoe UI', 10)),
                          cursor='hand2')
        
        def on_enter(event):
            button.config(bg=hover_bg)
            
        def on_leave(event):
            button.config(bg=default_bg)
            
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button
        
    def create_progress_dialog(self, title, message):
        """Create a progress dialog"""
        dialog = tk.Toplevel(self.parent)
        dialog.title(title)
        dialog.geometry("300x120")
        dialog.resizable(False, False)
        dialog.configure(bg='#1a1a2e')
        
        # Center dialog
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center on parent
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (300 // 2)
        y = (dialog.winfo_screenheight() // 2) - (120 // 2)
        dialog.geometry(f"300x120+{x}+{y}")
        
        # Message
        tk.Label(dialog, text=message, bg='#1a1a2e', fg='white',
                font=('Segoe UI', 10)).pack(pady=20)
        
        # Progress bar
        progress = ttk.Progressbar(dialog, mode='indeterminate')
        progress.pack(pady=10, padx=20, fill=tk.X)
        progress.start()
        
        return dialog, progress
