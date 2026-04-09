from datetime import datetime
from config import get_config

def calculate_days_until(abgabedatum_str):
    """Berechnet Tage bis zum Abgabedatum"""
    try:
        abgabedatum = datetime.strptime(abgabedatum_str, "%Y-%m-%d").date()
        heute = datetime.now().date()
        delta = (abgabedatum - heute).days
        return delta
    except:
        return None

def get_color(abgabedatum_str, eingabe_gemacht):
    """Bestimmt die Hintergrundfarbe basierend auf Konfiguration"""
    
    # Wenn keine Eingabe gemacht wurde: Grau
    if not eingabe_gemacht:
        return "#CCCCCC"  # Grau
    
    config = get_config()
    tage = calculate_days_until(abgabedatum_str)
    
    if tage is None:
        return "#FFFFFF"  # Weiß bei Fehler
    
    # Berechne Grenzen aus Konfiguration
    red_days = config["red_days"]
    orange_days = config["orange_weeks"] * 7
    green_weeks = config["green_weeks"] * 7
    
    # Farbe bestimmen
    if tage < red_days:
        return "#FF6B6B"  # Rot
    elif tage < orange_days:
        return "#FFA500"  # Orange
    elif tage <= green_weeks:
        return "#90EE90"  # Grün
    else:
        return "#FFFFFF"  # Weiß (mehr als Grün-Wochen)

def get_display_text(abgabedatum_str):
    """Zeigt an wie viele Tage/Wochen noch verbleibend sind"""
    tage = calculate_days_until(abgabedatum_str)
    
    if tage is None:
        return "Ungültiges Datum"
    
    if tage < 0:
        return f"⚠️ Abgelaufen ({abs(tage)} Tage)"
    elif tage == 0:
        return "🔴 Heute!"
    elif tage == 1:
        return "🔴 Morgen"
    elif tage < 7:
        return f"🔴 {tage} Tage"
    elif tage < 14:
        weeks = tage // 7
        return f"🟡 {weeks} Woche(n)"
    else:
        weeks = tage // 7
        return f"🟢 {weeks} Woche(n)"
