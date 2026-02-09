#!/usr/bin/env python3
“””
Screen Glitch Effect for Raspberry Pi OS
Erzeugt einen periodischen Glitch-Effekt mit Zittern und chromatischer Aberration
Löscht sich automatisch nach 1 Monat
“””

import time
import random
import subprocess
import signal
import sys
import os
from datetime import datetime, timedelta
import json

# Pfad zur Timestamp-Datei

TIMESTAMP_FILE = ‘/var/lib/screen-glitch-timestamp.json’
LIFESPAN_DAYS = 30  # Genau 1 Monat (30 Tage)

class ScreenGlitcher:
def **init**(self):
self.running = True
# Registriere Signal Handler für sauberes Beenden
signal.signal(signal.SIGINT, self.signal_handler)
signal.signal(signal.SIGTERM, self.signal_handler)

```
    # Prüfe oder erstelle Installations-Timestamp
    self.install_time = self.get_or_create_timestamp()
    
    # Prüfe ob Ablaufdatum erreicht ist
    if self.is_expired():
        print("Ablaufdatum erreicht. Starte Selbstzerstörung...")
        self.self_destruct()
        sys.exit(0)

def get_or_create_timestamp(self):
    """Erstellt oder liest den Installations-Timestamp"""
    try:
        if os.path.exists(TIMESTAMP_FILE):
            with open(TIMESTAMP_FILE, 'r') as f:
                data = json.load(f)
                return datetime.fromisoformat(data['install_time'])
        else:
            # Erste Installation - speichere aktuellen Zeitstempel
            now = datetime.now()
            os.makedirs(os.path.dirname(TIMESTAMP_FILE), exist_ok=True)
            with open(TIMESTAMP_FILE, 'w') as f:
                json.dump({'install_time': now.isoformat()}, f)
            return now
    except Exception as e:
        # Fallback: verwende aktuelles Datum
        return datetime.now()

def is_expired(self):
    """Prüft ob die Ablaufzeit erreicht ist"""
    expiry_date = self.install_time + timedelta(days=LIFESPAN_DAYS)
    return datetime.now() >= expiry_date

def self_destruct(self):
    """Löscht das Programm und alle zugehörigen Dateien"""
    try:
        print("Führe Selbstzerstörung durch...")
        
        # Stoppe den Service
        subprocess.run(['systemctl', 'stop', 'screen-glitch.service'], 
                     stderr=subprocess.DEVNULL)
        
        # Deaktiviere Autostart
        subprocess.run(['systemctl', 'disable', 'screen-glitch.service'], 
                     stderr=subprocess.DEVNULL)
        
        # Lösche Service-Datei
        service_file = '/etc/systemd/system/screen-glitch.service'
        if os.path.exists(service_file):
            os.remove(service_file)
        
        # Reload systemd
        subprocess.run(['systemctl', 'daemon-reload'], 
                     stderr=subprocess.DEVNULL)
        
        # Lösche Timestamp-Datei
        if os.path.exists(TIMESTAMP_FILE):
            os.remove(TIMESTAMP_FILE)
        
        # Lösche das Programm selbst
        script_path = '/usr/local/bin/screen_glitch.py'
        if os.path.exists(script_path):
            os.remove(script_path)
        
        print("Selbstzerstörung abgeschlossen. Alle Dateien wurden entfernt.")
        
    except Exception as e:
        print(f"Fehler bei der Selbstzerstörung: {e}")


def signal_handler(self, sig, frame):
    """Handle shutdown signals gracefully"""
    self.running = False
    self.reset_display()
    sys.exit(0)

def apply_glitch(self, intensity='medium'):
    """
    Wendet einen Glitch-Effekt auf den Bildschirm an
    intensity: 'low', 'medium', 'high'
    """
    try:
        # Offset-Werte für den Glitch-Effekt (in Pixel)
        offsets = {
            'low': (1, 2),
            'medium': (2, 4),
            'high': (3, 6)
        }
        
        x_offset, y_offset = offsets.get(intensity, offsets['medium'])
        
        # Zufällige Richtung
        x = random.choice([-x_offset, 0, x_offset])
        y = random.choice([-y_offset, 0, y_offset])
        
        # Verwende xrandr um den Bildschirm zu verschieben (Zitter-Effekt)
        # Hole zuerst die aktuelle Display-Konfiguration
        result = subprocess.run(['xrandr'], capture_output=True, text=True)
        
        # Finde den aktiven Display
        for line in result.stdout.split('\n'):
            if ' connected' in line and 'primary' in line:
                display_name = line.split()[0]
                
                # Wende Panning an für den Glitch-Effekt
                subprocess.run([
                    'xrandr',
                    '--output', display_name,
                    '--panning', f'1920x1080+{x}+{y}'
                ], stderr=subprocess.DEVNULL)
                break
        
        # Simuliere chromatische Aberration durch Farbverschiebung
        # (Hinweis: Dies erfordert redshift oder ähnliche Tools)
        # Als Alternative können wir Gamma-Werte anpassen
        self.apply_color_shift()
        
    except Exception as e:
        # Fehler ignorieren und weitermachen
        pass

def apply_color_shift(self):
    """Wendet eine Farbverschiebung an (Pink/Blau Effekt)"""
    try:
        # Zufällige Farbverschiebung für RGB-Kanäle
        # Werte > 1.0 verstärken, < 1.0 dämpfen den Kanal
        r = random.uniform(0.9, 1.2)  # Rot für Pink
        g = random.uniform(0.8, 1.0)  # Grün reduziert
        b = random.uniform(0.9, 1.2)  # Blau verstärkt
        
        # Verwende xrandr gamma Anpassung
        result = subprocess.run(['xrandr'], capture_output=True, text=True)
        
        for line in result.stdout.split('\n'):
            if ' connected' in line and 'primary' in line:
                display_name = line.split()[0]
                subprocess.run([
                    'xrandr',
                    '--output', display_name,
                    '--gamma', f'{r}:{g}:{b}'
                ], stderr=subprocess.DEVNULL)
                break
                
    except Exception:
        pass

def reset_display(self):
    """Setzt den Display zurück auf normale Werte"""
    try:
        result = subprocess.run(['xrandr'], capture_output=True, text=True)
        
        for line in result.stdout.split('\n'):
            if ' connected' in line and 'primary' in line:
                display_name = line.split()[0]
                
                # Reset panning
                subprocess.run([
                    'xrandr',
                    '--output', display_name,
                    '--panning', '0x0'
                ], stderr=subprocess.DEVNULL)
                
                # Reset gamma
                subprocess.run([
                    'xrandr',
                    '--output', display_name,
                    '--gamma', '1.0:1.0:1.0'
                ], stderr=subprocess.DEVNULL)
                break
                
    except Exception:
        pass

def run(self):
    """Hauptschleife des Glitch-Effekts"""
    print("Screen Glitcher gestartet... (Drücke Ctrl+C zum Beenden)")
    print(f"Installiert am: {self.install_time.strftime('%d.%m.%Y %H:%M:%S')}")
    expiry_date = self.install_time + timedelta(days=LIFESPAN_DAYS)
    print(f"Läuft ab am: {expiry_date.strftime('%d.%m.%Y %H:%M:%S')}")
    
    while self.running:
        try:
            # Prüfe bei jedem Durchlauf ob abgelaufen
            if self.is_expired():
                print("\nAblaufdatum erreicht!")
                self.self_destruct()
                break
            
            # Zufällige Pause zwischen Glitches (3-10 Sekunden)
            wait_time = random.uniform(3.0, 10.0)
            time.sleep(wait_time)
            
            # Wähle zufällige Intensität
            intensity = random.choice(['low', 'medium', 'medium', 'high'])
            
            # Wende Glitch an
            self.apply_glitch(intensity)
            
            # Glitch-Dauer (0.05 - 0.3 Sekunden)
            glitch_duration = random.uniform(0.05, 0.3)
            time.sleep(glitch_duration)
            
            # Setze Display zurück
            self.reset_display()
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            # Bei Fehler kurz warten und weitermachen
            time.sleep(1)
    
    # Cleanup beim Beenden
    self.reset_display()
    print("\nScreen Glitcher beendet.")
```

if **name** == ‘**main**’:
glitcher = ScreenGlitcher()
glitcher.run()
