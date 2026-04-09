import tkinter as tk
from tkinter import ttk, messagebox
from database import init_database, get_all_offerten, add_offerte, update_offerte, delete_offerte
from utils.colors import get_color, get_display_text
from ui.settings_window import SettingsWindow
from ui.offerte_dialog import OffertDialog

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Offerte-Manager")
        self.root.geometry("1200x600")
        init_database()
        self.init_ui()
        self.load_offerten()
    
    def init_ui(self):
        """Initialisiert die Benutzeroberfläche"""
        # Hauptframe
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tabelle (Treeview) mit Scrollbar
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Name", "Eingangsdatum", "Abgabedatum", "Verbleibende Zeit", "Eingabe gemacht"),
            height=20,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)
        
        # Spalten konfigurieren
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("ID", anchor=tk.CENTER, width=50)
        self.tree.column("Name", anchor=tk.W, width=200)
        self.tree.column("Eingangsdatum", anchor=tk.CENTER, width=120)
        self.tree.column("Abgabedatum", anchor=tk.CENTER, width=120)
        self.tree.column("Verbleibende Zeit", anchor=tk.CENTER, width=180)
        self.tree.column("Eingabe gemacht", anchor=tk.CENTER, width=150)
        
        # Header
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.tree.heading("Name", text="Name", anchor=tk.W)
        self.tree.heading("Eingangsdatum", text="Eingangsdatum", anchor=tk.CENTER)
        self.tree.heading("Abgabedatum", text="Abgabedatum", anchor=tk.CENTER)
        self.tree.heading("Verbleibende Zeit", text="Verbleibende Zeit", anchor=tk.CENTER)
        self.tree.heading("Eingabe gemacht", text="Eingabe gemacht", anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Tags für Farben definieren
        self.tree.tag_configure("gruen", background="#90EE90")
        self.tree.tag_configure("orange", background="#FFA500")
        self.tree.tag_configure("rot", background="#FF6B6B")
        self.tree.tag_configure("grau", background="#CCCCCC")
        self.tree.tag_configure("weiss", background="#FFFFFF")
        
        # Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=0, pady=10)
        
        tk.Button(button_frame, text="➕ Neue Offerte", command=self.add_offerte, width=20, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="✏️ Bearbeiten", command=self.edit_offerte, width=20, bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="🗑️ Löschen", command=self.delete_offerte, width=20, bg="#f44336", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="🔄 Aktualisieren", command=self.load_offerten, width=20, bg="#FF9800", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="⚙️ Einstellungen", command=self.open_settings, width=20, bg="#9C27B0", fg="white").pack(side=tk.LEFT, padx=5)
    
    def load_offerten(self):
        """Lädt alle Offerten in die Tabelle"""
        # Alte Einträge löschen
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        offerten = get_all_offerten()
        
        for offerte in offerten:
            offerte_id, name, eingangsdatum, abgabedatum, eingabe_gemacht, _ = offerte
            
            # Farbe und Text bestimmen
            color_hex = get_color(abgabedatum, eingabe_gemacht)
            display_text = get_display_text(abgabedatum)
            eingabe_text = "✅ Ja" if eingabe_gemacht else "❌ Nein"
            
            # Tag basierend auf Farbe
            if color_hex == "#90EE90":
                tag = "gruen"
            elif color_hex == "#FFA500":
                tag = "orange"
            elif color_hex == "#FF6B6B":
                tag = "rot"
            elif color_hex == "#CCCCCC":
                tag = "grau"
            else:
                tag = "weiss"
            
            values = (offerte_id, name, eingangsdatum, abgabedatum, display_text, eingabe_text)
            self.tree.insert(parent='', index='end', text='', values=values, tags=(tag,))
    
    def add_offerte(self):
        """Öffnet Dialog zum Hinzufügen einer neuen Offerte"""
        dialog = OffertDialog(self.root)
        if dialog.result:
            name, eingangsdatum, abgabedatum, eingabe_gemacht = dialog.result
            add_offerte(name, eingangsdatum, abgabedatum, eingabe_gemacht)
            self.load_offerten()
    
    def edit_offerte(self):
        """Bearbeitet die ausgewählte Offerte"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warnung", "Bitte wählen Sie eine Offerte aus!")
            return
        
        item = self.tree.item(selected[0])
        offerte_id = item['values'][0]
        offerten = get_all_offerten()
        offerte = [o for o in offerten if o[0] == offerte_id][0]
        
        dialog = OffertDialog(self.root, offerte)
        if dialog.result:
            name, eingangsdatum, abgabedatum, eingabe_gemacht = dialog.result
            update_offerte(offerte_id, name, eingangsdatum, abgabedatum, eingabe_gemacht)
            self.load_offerten()
    
    def delete_offerte(self):
        """Löscht die ausgewählte Offerte"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warnung", "Bitte wählen Sie eine Offerte aus!")
            return
        
        if messagebox.askyesno("Bestätigung", "Möchten Sie diese Offerte wirklich löschen?"):
            item = self.tree.item(selected[0])
            offerte_id = item['values'][0]
            delete_offerte(offerte_id)
            self.load_offerten()
    
    def open_settings(self):
        """Öffnet das Einstellungsfenster"""
        SettingsWindow(self.root, self.load_offerten)
