import tkinter as tk
from config import load_config, save_config

class SettingsWindow:
    def __init__(self, parent, callback=None):
        self.callback = callback
        self.config = load_config()
        
        self.window = tk.Toplevel(parent)
        self.window.title("Einstellungen")
        self.window.geometry("450x350")
        self.window.transient(parent)
        self.window.grab_set()
        
        self.init_ui()
    
    def init_ui(self):
        """Initialisiert das Einstellungsfenster"""
        frame = tk.Frame(self.window)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titel
        title = tk.Label(frame, text="Farbcodierung anpassen", font=("Arial", 14, "bold"))
        title.pack(anchor=tk.W, pady=(0, 20))
        
        # Grüne Wochen
        tk.Label(frame, text="🟢 Grüne Warnung (Wochen):", font=("Arial", 10)).pack(anchor=tk.W, pady=(10, 5))
        tk.Label(frame, text="Wenn noch MEHR als diese Wochen verbleibend sind", font=("Arial", 8, "italic")).pack(anchor=tk.W, padx=20)
        self.green_var = tk.IntVar(value=self.config["green_weeks"])
        tk.Spinbox(frame, from_=1, to=12, textvariable=self.green_var, width=10, font=("Arial", 10)).pack(anchor=tk.W, padx=20, pady=(0, 15))
        
        # Orange Wochen
        tk.Label(frame, text="🟡 Orange Warnung (Wochen):", font=("Arial", 10)).pack(anchor=tk.W, pady=(10, 5))
        tk.Label(frame, text="Wenn noch WENIGER als diese Wochen verbleibend sind", font=("Arial", 8, "italic")).pack(anchor=tk.W, padx=20)
        self.orange_var = tk.IntVar(value=self.config["orange_weeks"])
        tk.Spinbox(frame, from_=1, to=12, textvariable=self.orange_var, width=10, font=("Arial", 10)).pack(anchor=tk.W, padx=20, pady=(0, 15))
        
        # Rote Tage
        tk.Label(frame, text="🔴 Rote Warnung (Tage):", font=("Arial", 10)).pack(anchor=tk.W, pady=(10, 5))
        tk.Label(frame, text="Wenn noch WENIGER als diese Tage verbleibend sind", font=("Arial", 8, "italic")).pack(anchor=tk.W, padx=20)
        self.red_var = tk.IntVar(value=self.config["red_days"])
        tk.Spinbox(frame, from_=1, to=30, textvariable=self.red_var, width=10, font=("Arial", 10)).pack(anchor=tk.W, padx=20, pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        tk.Button(button_frame, text="💾 Speichern", command=self.save_settings, width=20, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="❌ Abbrechen", command=self.window.destroy, width=20, bg="#f44336", fg="white").pack(side=tk.LEFT, padx=5)
    
    def save_settings(self):
        """Speichert die neuen Einstellungen"""
        self.config["green_weeks"] = self.green_var.get()
        self.config["orange_weeks"] = self.orange_var.get()
        self.config["red_days"] = self.red_var.get()
        save_config(self.config)
        
        if self.callback:
            self.callback()
        
        self.window.destroy()
