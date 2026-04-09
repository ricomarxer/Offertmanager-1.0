import tkinter as tk
from datetime import datetime
from tkinter import messagebox

class OffertDialog:
    def __init__(self, parent, offerte=None):
        self.result = None
        self.offerte = offerte
        
        self.window = tk.Toplevel(parent)
        if offerte:
            self.window.title("Offerte bearbeiten")
        else:
            self.window.title("Neue Offerte")
        
        self.window.geometry("450x350")
        self.window.transient(parent)
        self.window.grab_set()
        
        self.init_ui()
        parent.wait_window(self.window)
    
    def init_ui(self):
        """Initialisiert den Dialog"""
        frame = tk.Frame(self.window)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Name
        tk.Label(frame, text="Offertenname:", font=("Arial", 10)).pack(anchor=tk.W, pady=(0, 5))
        self.name_input = tk.Entry(frame, width=40, font=("Arial", 10))
        if self.offerte:
            self.name_input.insert(0, self.offerte[1])
        self.name_input.pack(anchor=tk.W, pady=(0, 15))
        
        # Eingangsdatum
        tk.Label(frame, text="Eingangsdatum (YYYY-MM-DD):", font=("Arial", 10)).pack(anchor=tk.W, pady=(0, 5))
        self.eingangsdatum_input = tk.Entry(frame, width=40, font=("Arial", 10))
        if self.offerte:
            self.eingangsdatum_input.insert(0, self.offerte[2])
        else:
            self.eingangsdatum_input.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.eingangsdatum_input.pack(anchor=tk.W, pady=(0, 15))
        
        # Abgabedatum
        tk.Label(frame, text="Abgabedatum (YYYY-MM-DD):", font=("Arial", 10)).pack(anchor=tk.W, pady=(0, 5))
        self.abgabedatum_input = tk.Entry(frame, width=40, font=("Arial", 10))
        if self.offerte:
            self.abgabedatum_input.insert(0, self.offerte[3])
        else:
            self.abgabedatum_input.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.abgabedatum_input.pack(anchor=tk.W, pady=(0, 15))
        
        # Eingabe gemacht
        self.eingabe_var = tk.BooleanVar(value=False)
        if self.offerte and self.offerte[4]:
            self.eingabe_var.set(True)
        tk.Checkbutton(frame, text="✅ Offerteingabe gemacht", variable=self.eingabe_var, font=("Arial", 10)).pack(anchor=tk.W, pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        tk.Button(button_frame, text="💾 Speichern", command=self.save, width=20, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="❌ Abbrechen", command=self.window.destroy, width=20, bg="#f44336", fg="white").pack(side=tk.LEFT, padx=5)
    
    def save(self):
        """Speichert die Daten"""
        name = self.name_input.get().strip()
        eingangsdatum = self.eingangsdatum_input.get().strip()
        abgabedatum = self.abgabedatum_input.get().strip()
        
        # Validierung
        if not name:
            messagebox.showerror("Fehler", "Bitte geben Sie einen Namen ein!")
            return
        
        try:
            datetime.strptime(eingangsdatum, "%Y-%m-%d")
            datetime.strptime(abgabedatum, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Fehler", "Bitte verwenden Sie das Format YYYY-MM-DD für Daten!")
            return
        
        self.result = (name, eingangsdatum, abgabedatum, self.eingabe_var.get())
        self.window.destroy()
