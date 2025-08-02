"""
Advanced Password Generator - Main Application
A professional-grade password generator with GUI interface
Author: OMM Projects
Version: 2.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime
from password_core import PasswordGenerator
from security_utils import PasswordAnalyzer
from gui_components import CustomWidgets

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.generator = PasswordGenerator()
        self.analyzer = PasswordAnalyzer()
        self.custom_widgets = CustomWidgets(root)
        
        # Variables
        self.setup_variables()
        self.create_gui()
        self.load_settings()
        
    def setup_window(self):
        """Configure main window properties"""
        self.root.title("🔐 Advanced Password Generator | OMM Projects")
        self.root.geometry("800x600")
        self.root.minsize(600, 500)
        self.root.configure(bg='#1a1a2e')
        
        # Set icon if available
        try:
            self.root.iconbitmap('assets/icon.ico')
        except:
            pass
            
        # Center window
        self.center_window()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"800x600+{x}+{y}")
        
    def setup_variables(self):
        """Initialize tkinter variables"""
        self.password_length = tk.IntVar(value=16)
        self.include_uppercase = tk.BooleanVar(value=True)
        self.include_lowercase = tk.BooleanVar(value=True)
        self.include_numbers = tk.BooleanVar(value=True)
        self.include_symbols = tk.BooleanVar(value=True)
        self.exclude_similar = tk.BooleanVar(value=False)
        self.custom_chars = tk.StringVar()
        self.generated_password = tk.StringVar()
        
    def create_gui(self):
        """Create the main GUI interface"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(title_frame, 
                              text="🔐 Advanced Password Generator",
                              font=("Segoe UI", 24, "bold"),
                              fg="#00d4ff", bg="#1a1a2e")
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame,
                                 text="Generate secure passwords with advanced customization",
                                 font=("Segoe UI", 10),
                                 fg="#888", bg="#1a1a2e")
        subtitle_label.pack()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Generator tab
        self.create_generator_tab()
        
        # Batch generator tab
        self.create_batch_tab()
        
        # Analyzer tab
        self.create_analyzer_tab()
        
        # Settings tab
        self.create_settings_tab()
        
    def create_generator_tab(self):
        """Create the main password generator tab"""
        gen_frame = ttk.Frame(self.notebook)
        self.notebook.add(gen_frame, text="🔑 Generator")
        
        # Configuration frame
        config_frame = ttk.LabelFrame(gen_frame, text="Password Configuration", padding=15)
        config_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Length slider
        length_frame = ttk.Frame(config_frame)
        length_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(length_frame, text="Password Length:").pack(side=tk.LEFT)
        length_value_label = ttk.Label(length_frame, textvariable=self.password_length)
        length_value_label.pack(side=tk.RIGHT)
        
        length_scale = ttk.Scale(config_frame, 
                                from_=4, to=128, 
                                variable=self.password_length,
                                orient=tk.HORIZONTAL)
        length_scale.pack(fill=tk.X, pady=5)
        
        # Character options
        options_frame = ttk.Frame(config_frame)
        options_frame.pack(fill=tk.X, pady=10)
        
        # Left column
        left_options = ttk.Frame(options_frame)
        left_options.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Checkbutton(left_options, text="Uppercase Letters (A-Z)", 
                       variable=self.include_uppercase).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(left_options, text="Lowercase Letters (a-z)", 
                       variable=self.include_lowercase).pack(anchor=tk.W, pady=2)
        
        # Right column
        right_options = ttk.Frame(options_frame)
        right_options.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        ttk.Checkbutton(right_options, text="Numbers (0-9)", 
                       variable=self.include_numbers).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(right_options, text="Special Characters (!@#$)", 
                       variable=self.include_symbols).pack(anchor=tk.W, pady=2)
        
        # Advanced options
        advanced_frame = ttk.Frame(config_frame)
        advanced_frame.pack(fill=tk.X, pady=5)
        
        ttk.Checkbutton(advanced_frame, text="Exclude Similar Characters (0, O, l, 1)", 
                       variable=self.exclude_similar).pack(anchor=tk.W)
        
        # Custom characters
        custom_frame = ttk.Frame(config_frame)
        custom_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(custom_frame, text="Custom Characters:").pack(anchor=tk.W)
        custom_entry = ttk.Entry(custom_frame, textvariable=self.custom_chars)
        custom_entry.pack(fill=tk.X, pady=2)
        
        # Generate button
        generate_btn = tk.Button(config_frame,
                                text="🎲 Generate Password",
                                command=self.generate_password,
                                bg="#00d4ff", fg="white",
                                font=("Segoe UI", 12, "bold"),
                                relief=tk.FLAT, pady=10)
        generate_btn.pack(fill=tk.X, pady=10)
        
        # Result frame
        result_frame = ttk.LabelFrame(gen_frame, text="Generated Password", padding=15)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        # Password display
        password_display = tk.Text(result_frame, height=3, font=("Courier New", 14, "bold"),
                                  wrap=tk.WORD, bg="#2a2a3e", fg="#00ff88", relief=tk.FLAT)
        password_display.pack(fill=tk.X, pady=(0, 10))
        self.password_display = password_display
        
        # Buttons frame
        buttons_frame = ttk.Frame(result_frame)
        buttons_frame.pack(fill=tk.X)
        
        copy_btn = ttk.Button(buttons_frame, text="📋 Copy", 
                             command=self.copy_password)
        copy_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        save_btn = ttk.Button(buttons_frame, text="💾 Save", 
                             command=self.save_password)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        analyze_btn = ttk.Button(buttons_frame, text="🔍 Analyze", 
                               command=self.analyze_current_password)
        analyze_btn.pack(side=tk.LEFT, padx=5)
        
        # Strength indicator
        strength_frame = ttk.Frame(result_frame)
        strength_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(strength_frame, text="Password Strength:").pack(side=tk.LEFT)
        
        self.strength_progress = ttk.Progressbar(strength_frame, length=200)
        self.strength_progress.pack(side=tk.RIGHT, padx=(10, 0))
        
        self.strength_label = ttk.Label(strength_frame, text="")
        self.strength_label.pack(side=tk.RIGHT, padx=(10, 0))
        
    def create_batch_tab(self):
        """Create batch password generation tab"""
        batch_frame = ttk.Frame(self.notebook)
        self.notebook.add(batch_frame, text="📦 Batch Generator")
        
        # Configuration
        config_frame = ttk.LabelFrame(batch_frame, text="Batch Configuration", padding=15)
        config_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Number of passwords
        count_frame = ttk.Frame(config_frame)
        count_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(count_frame, text="Number of Passwords:").pack(side=tk.LEFT)
        self.batch_count = tk.IntVar(value=10)
        count_spin = ttk.Spinbox(count_frame, from_=1, to=1000, 
                                textvariable=self.batch_count, width=10)
        count_spin.pack(side=tk.RIGHT)
        
        # Generate button
        batch_generate_btn = tk.Button(config_frame,
                                      text="🎲 Generate Multiple Passwords",
                                      command=self.generate_batch_passwords,
                                      bg="#00d4ff", fg="white",
                                      font=("Segoe UI", 12, "bold"),
                                      relief=tk.FLAT, pady=10)
        batch_generate_btn.pack(fill=tk.X, pady=10)
        
        # Results
        results_frame = ttk.LabelFrame(batch_frame, text="Generated Passwords", padding=15)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Text area with scrollbar
        text_frame = ttk.Frame(results_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.batch_text = tk.Text(text_frame, font=("Courier New", 10),
                                 bg="#2a2a3e", fg="#00ff88", relief=tk.FLAT)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.batch_text.yview)
        self.batch_text.configure(yscrollcommand=scrollbar.set)
        
        self.batch_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Export buttons
        export_frame = ttk.Frame(results_frame)
        export_frame.pack(fill=tk.X, pady=(10, 0))
        
        export_txt_btn = ttk.Button(export_frame, text="📄 Export as TXT", 
                                   command=self.export_txt)
        export_txt_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        export_csv_btn = ttk.Button(export_frame, text="📊 Export as CSV", 
                                   command=self.export_csv)
        export_csv_btn.pack(side=tk.LEFT, padx=5)
        
    def create_analyzer_tab(self):
        """Create password analyzer tab"""
        analyzer_frame = ttk.Frame(self.notebook)
        self.notebook.add(analyzer_frame, text="🔍 Analyzer")
        
        # Input frame
        input_frame = ttk.LabelFrame(analyzer_frame, text="Password Analysis", padding=15)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(input_frame, text="Enter password to analyze:").pack(anchor=tk.W)
        
        self.analyze_entry = tk.Entry(input_frame, font=("Courier New", 12), 
                                     show="*", bg="#2a2a3e", fg="white", relief=tk.FLAT)
        self.analyze_entry.pack(fill=tk.X, pady=5)
        
        # Show/hide password
        show_frame = ttk.Frame(input_frame)
        show_frame.pack(fill=tk.X, pady=5)
        
        self.show_password = tk.BooleanVar()
        show_check = ttk.Checkbutton(show_frame, text="Show Password", 
                                    variable=self.show_password,
                                    command=self.toggle_password_visibility)
        show_check.pack(side=tk.LEFT)
        
        analyze_btn = tk.Button(show_frame,
                               text="🔍 Analyze",
                               command=self.analyze_password,
                               bg="#ff6b35", fg="white",
                               font=("Segoe UI", 10, "bold"),
                               relief=tk.FLAT)
        analyze_btn.pack(side=tk.RIGHT)
        
        # Results frame
        results_frame = ttk.LabelFrame(analyzer_frame, text="Analysis Results", padding=15)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.analysis_text = tk.Text(results_frame, font=("Segoe UI", 10),
                                    bg="#2a2a3e", fg="#ffffff", relief=tk.FLAT,
                                    state=tk.DISABLED)
        self.analysis_text.pack(fill=tk.BOTH, expand=True)
        
    def create_settings_tab(self):
        """Create settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # General settings
        general_frame = ttk.LabelFrame(settings_frame, text="General Settings", padding=15)
        general_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Auto-copy setting
        self.auto_copy = tk.BooleanVar(value=True)
        ttk.Checkbutton(general_frame, text="Auto-copy generated passwords", 
                       variable=self.auto_copy).pack(anchor=tk.W, pady=2)
        
        # Save history setting
        self.save_history = tk.BooleanVar(value=True)
        ttk.Checkbutton(general_frame, text="Save password generation history", 
                       variable=self.save_history).pack(anchor=tk.W, pady=2)
        
        # Security settings
        security_frame = ttk.LabelFrame(settings_frame, text="Security Settings", padding=15)
        security_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Clear clipboard setting
        self.clear_clipboard = tk.BooleanVar(value=False)
        ttk.Checkbutton(security_frame, text="Clear clipboard after 30 seconds", 
                       variable=self.clear_clipboard).pack(anchor=tk.W, pady=2)
        
        # Buttons
        buttons_frame = ttk.Frame(settings_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        save_settings_btn = ttk.Button(buttons_frame, text="💾 Save Settings", 
                                     command=self.save_settings)
        save_settings_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        reset_btn = ttk.Button(buttons_frame, text="🔄 Reset to Defaults", 
                              command=self.reset_settings)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # About section
        about_frame = ttk.LabelFrame(settings_frame, text="About", padding=15)
        about_frame.pack(fill=tk.BOTH, expand=True)
        
        about_text = """
Advanced Password Generator v2.0.0

Developed by: OMM Projects
GitHub: github.com/omm-projects
Website: projects-omm.space

Features:
• Secure password generation with customizable options
• Batch password generation
• Password strength analysis
• Export functionality
• Security-focused design

This tool helps you create strong, unique passwords to keep your accounts secure.
        """
        
        about_label = tk.Label(about_frame, text=about_text, 
                              justify=tk.LEFT, bg="#1a1a2e", fg="#888")
        about_label.pack(anchor=tk.W)
        
    def generate_password(self):
        """Generate a single password"""
        try:
            options = {
                'length': self.password_length.get(),
                'uppercase': self.include_uppercase.get(),
                'lowercase': self.include_lowercase.get(),
                'numbers': self.include_numbers.get(),
                'symbols': self.include_symbols.get(),
                'exclude_similar': self.exclude_similar.get(),
                'custom_chars': self.custom_chars.get()
            }
            
            password = self.generator.generate(options)
            
            self.password_display.delete(1.0, tk.END)
            self.password_display.insert(1.0, password)
            
            # Update strength indicator
            strength_info = self.analyzer.analyze_strength(password)
            self.update_strength_indicator(strength_info)
            
            # Auto-copy if enabled
            if self.auto_copy.get():
                self.copy_password()
                
            # Save to history
            if self.save_history.get():
                self.save_to_history(password, options)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate password: {str(e)}")
            
    def generate_batch_passwords(self):
        """Generate multiple passwords"""
        try:
            count = self.batch_count.get()
            options = {
                'length': self.password_length.get(),
                'uppercase': self.include_uppercase.get(),
                'lowercase': self.include_lowercase.get(),
                'numbers': self.include_numbers.get(),
                'symbols': self.include_symbols.get(),
                'exclude_similar': self.exclude_similar.get(),
                'custom_chars': self.custom_chars.get()
            }
            
            passwords = []
            for i in range(count):
                password = self.generator.generate(options)
                passwords.append(f"{i+1:3d}. {password}")
                
            self.batch_text.delete(1.0, tk.END)
            self.batch_text.insert(1.0, "\n".join(passwords))
            
            self.batch_passwords = [p.split(". ", 1)[1] for p in passwords]
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate batch passwords: {str(e)}")
            
    def copy_password(self):
        """Copy current password to clipboard"""
        try:
            password = self.password_display.get(1.0, tk.END).strip()
            if password:
                self.root.clipboard_clear()
                self.root.clipboard_append(password)
                messagebox.showinfo("Success", "Password copied to clipboard!")
                
                # Clear clipboard after 30 seconds if enabled
                if self.clear_clipboard.get():
                    self.root.after(30000, self.clear_clipboard_delayed)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy password: {str(e)}")
            
    def clear_clipboard_delayed(self):
        """Clear clipboard after delay"""
        self.root.clipboard_clear()
        
    def save_password(self):
        """Save current password to file"""
        try:
            password = self.password_display.get(1.0, tk.END).strip()
            if not password:
                messagebox.showwarning("Warning", "No password to save!")
                return
                
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if filename:
                with open(filename, 'w') as f:
                    f.write(f"Generated Password: {password}\n")
                    f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Length: {len(password)}\n")
                    
                messagebox.showinfo("Success", f"Password saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save password: {str(e)}")
            
    def analyze_current_password(self):
        """Analyze the currently generated password"""
        password = self.password_display.get(1.0, tk.END).strip()
        if password:
            self.analyze_entry.delete(0, tk.END)
            self.analyze_entry.insert(0, password)
            self.notebook.select(2)  # Switch to analyzer tab
            self.analyze_password()
            
    def analyze_password(self):
        """Analyze entered password"""
        password = self.analyze_entry.get()
        if not password:
            messagebox.showwarning("Warning", "Please enter a password to analyze!")
            return
            
        analysis = self.analyzer.full_analysis(password)
        
        self.analysis_text.config(state=tk.NORMAL)
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(1.0, analysis)
        self.analysis_text.config(state=tk.DISABLED)
        
    def toggle_password_visibility(self):
        """Toggle password visibility in analyzer"""
        if self.show_password.get():
            self.analyze_entry.config(show="")
        else:
            self.analyze_entry.config(show="*")
            
    def update_strength_indicator(self, strength_info):
        """Update password strength indicator"""
        score = strength_info.get('score', 0)
        level = strength_info.get('level', 'Unknown')
        
        self.strength_progress['value'] = score
        self.strength_label.config(text=level)
        
        # Color coding
        colors = {'Very Weak': 'red', 'Weak': 'orange', 'Fair': 'yellow', 
                 'Good': 'lightgreen', 'Strong': 'green', 'Very Strong': 'darkgreen'}
        
    def export_txt(self):
        """Export batch passwords to TXT file"""
        try:
            if not hasattr(self, 'batch_passwords') or not self.batch_passwords:
                messagebox.showwarning("Warning", "No passwords to export!")
                return
                
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if filename:
                with open(filename, 'w') as f:
                    f.write(f"Generated Passwords - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 50 + "\n\n")
                    for i, password in enumerate(self.batch_passwords, 1):
                        f.write(f"{i:3d}. {password}\n")
                        
                messagebox.showinfo("Success", f"Passwords exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export passwords: {str(e)}")
            
    def export_csv(self):
        """Export batch passwords to CSV file"""
        try:
            if not hasattr(self, 'batch_passwords') or not self.batch_passwords:
                messagebox.showwarning("Warning", "No passwords to export!")
                return
                
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filename:
                import csv
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Index", "Password", "Length", "Generated_Time"])
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    for i, password in enumerate(self.batch_passwords, 1):
                        writer.writerow([i, password, len(password), timestamp])
                        
                messagebox.showinfo("Success", f"Passwords exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export passwords: {str(e)}")
            
    def save_to_history(self, password, options):
        """Save password generation to history"""
        try:
            history_entry = {
                'password': password,
                'options': options,
                'timestamp': datetime.now().isoformat(),
                'length': len(password)
            }
            
            history_file = 'password_history.json'
            history = []
            
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    history = json.load(f)
                    
            history.append(history_entry)
            
            # Keep only last 100 entries
            history = history[-100:]
            
            with open(history_file, 'w') as f:
                json.dump(history, f, indent=2)
                
        except Exception as e:
            print(f"Failed to save history: {e}")
            
    def load_settings(self):
        """Load application settings"""
        try:
            settings_file = 'settings.json'
            if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
                    
                self.auto_copy.set(settings.get('auto_copy', True))
                self.save_history.set(settings.get('save_history', True))
                self.clear_clipboard.set(settings.get('clear_clipboard', False))
                
        except Exception as e:
            print(f"Failed to load settings: {e}")
            
    def save_settings(self):
        """Save application settings"""
        try:
            settings = {
                'auto_copy': self.auto_copy.get(),
                'save_history': self.save_history.get(),
                'clear_clipboard': self.clear_clipboard.get()
            }
            
            with open('settings.json', 'w') as f:
                json.dump(settings, f, indent=2)
                
            messagebox.showinfo("Success", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
            
    def reset_settings(self):
        """Reset settings to defaults"""
        self.auto_copy.set(True)
        self.save_history.set(True)
        self.clear_clipboard.set(False)
        messagebox.showinfo("Success", "Settings reset to defaults!")


def main():
    """Main application entry point"""
    root = tk.Tk()
    
    # Apply dark theme
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure colors
    style.configure('TFrame', background='#1a1a2e')
    style.configure('TLabel', background='#1a1a2e', foreground='#ffffff')
    style.configure('TLabelFrame', background='#1a1a2e', foreground='#00d4ff')
    style.configure('TLabelFrame.Label', background='#1a1a2e', foreground='#00d4ff')
    style.configure('TButton', background='#16213e', foreground='#ffffff')
    style.configure('TCheckbutton', background='#1a1a2e', foreground='#ffffff')
    style.configure('TEntry', fieldbackground='#2a2a3e', foreground='#ffffff')
    style.configure('TScale', background='#1a1a2e')
    style.configure('TSpinbox', fieldbackground='#2a2a3e', foreground='#ffffff')
    style.configure('TNotebook', background='#1a1a2e')
    style.configure('TNotebook.Tab', background='#16213e', foreground='#ffffff')
    
    root.configure(bg='#1a1a2e')
    
    app = PasswordGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
