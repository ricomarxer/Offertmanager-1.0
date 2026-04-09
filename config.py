import json
import os
from pathlib import Path

CONFIG_FILE = "settings.json"

DEFAULT_CONFIG = {
    "green_weeks": 2,
    "orange_weeks": 1,
    "red_days": 2,
    "onedrive_path": str(Path.home() / "OneDrive"),
    "database_path": "offerte_data.db"
}

def load_config():
    """Lädt Einstellungen aus JSON-Datei"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return DEFAULT_CONFIG

def save_config(config):
    """Speichert Einstellungen in JSON-Datei"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

def get_config():
    """Gibt aktuelle Konfiguration zurück"""
    return load_config()
