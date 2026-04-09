import sqlite3
from config import get_config

def get_database_path():
    """Gibt den Pfad zur Datenbank zurück"""
    config = get_config()
    return config["database_path"]

def init_database():
    """Erstellt die Datenbanktabelle beim ersten Start"""
    conn = sqlite3.connect(get_database_path())
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS offerten (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            eingangsdatum TEXT NOT NULL,
            abgabedatum TEXT NOT NULL,
            eingabe_gemacht INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def add_offerte(name, eingangsdatum, abgabedatum, eingabe_gemacht):
    """Fügt eine neue Offerte hinzu"""
    conn = sqlite3.connect(get_database_path())
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO offerten (name, eingangsdatum, abgabedatum, eingabe_gemacht)
        VALUES (?, ?, ?, ?)
    ''', (name, eingangsdatum, abgabedatum, int(eingabe_gemacht)))
    
    conn.commit()
    conn.close()

def get_all_offerten():
    """Ruft alle Offerten ab"""
    conn = sqlite3.connect(get_database_path())
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM offerten ORDER BY abgabedatum ASC')
    offerten = cursor.fetchall()
    conn.close()
    return offerten

def update_offerte(offerte_id, name, eingangsdatum, abgabedatum, eingabe_gemacht):
    """Aktualisiert eine Offerte"""
    conn = sqlite3.connect(get_database_path())
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE offerten 
        SET name=?, eingangsdatum=?, abgabedatum=?, eingabe_gemacht=?
        WHERE id=?
    ''', (name, eingangsdatum, abgabedatum, int(eingabe_gemacht), offerte_id))
    
    conn.commit()
    conn.close()

def delete_offerte(offerte_id):
    """Löscht eine Offerte"""
    conn = sqlite3.connect(get_database_path())
    cursor = conn.cursor()
    cursor.execute('DELETE FROM offerten WHERE id=?', (offerte_id,))
    conn.commit()
    conn.close()
