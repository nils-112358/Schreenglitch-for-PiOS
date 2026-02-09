# Screen Glitch Effect für Raspberry Pi OS

Ein Programm, das einen periodischen Glitch-Effekt auf dem Bildschirm erzeugt mit:

- Zitter-/Shake-Effekt
- Chromatischer Aberration (Pink/Blau Farbverschiebung)
- Zufälligen Intervallen und Intensitäten
- **Automatischer Selbstzerstörung nach genau 30 Tagen**

## ⚠️ WICHTIG: Automatische Löschung

**Das Programm löscht sich automatisch nach genau 30 Tagen (1 Monat)!**

- Der Installationszeitpunkt wird beim ersten Start gespeichert
- Nach 30 Tagen deinstalliert sich das Programm vollständig
- Alle Dateien werden automatisch entfernt:
  - `/usr/local/bin/screen_glitch.py` (das Hauptprogramm)
  - `/etc/systemd/system/screen-glitch.service` (der Service)
  - `/var/lib/screen-glitch-timestamp.json` (der Zeitstempel)
- Der Autostart wird deaktiviert
- Keine manuellen Schritte notwendig

## Installation

### 1. Dateien vorbereiten

Stelle sicher, dass beide Dateien ausführbar sind:

```bash
chmod +x screen_glitch.py
chmod +x install.sh
```

### 2. Installation ausführen

```bash
sudo ./install.sh
```

Das Script wird:

- Das Python-Programm nach `/usr/local/bin` kopieren
- Einen systemd Service erstellen
- Den Service aktivieren und starten
- Den Autostart konfigurieren

## Verwendung

### Service-Befehle

**Status überprüfen:**

```bash
sudo systemctl status screen-glitch
```

**Service stoppen:**

```bash
sudo systemctl stop screen-glitch
```

**Service starten:**

```bash
sudo systemctl start screen-glitch
```

**Autostart deaktivieren:**

```bash
sudo systemctl disable screen-glitch
```

**Service neu starten:**

```bash
sudo systemctl restart screen-glitch
```

### Logs ansehen

```bash
sudo journalctl -u screen-glitch -f
```

### Installationszeitpunkt prüfen

Um zu sehen, wann das Programm installiert wurde und wann es sich löscht:

```bash
cat /var/lib/screen-glitch-timestamp.json
```

Oder direkt beim Service-Status:

```bash
sudo journalctl -u screen-glitch | grep "Installiert am"
```

### Ablaufdatum ändern

Wenn du die 30-Tage-Frist ändern möchtest, bearbeite diese Zeile in `/usr/local/bin/screen_glitch.py` (Zeile 13):

```python
LIFESPAN_DAYS = 30  # Genau 1 Monat (30 Tage)
```

Ändere `30` auf die gewünschte Anzahl Tage. Nach der Änderung:

```bash
sudo systemctl restart screen-glitch
```

**Hinweis:** Wenn du die Timestamp-Datei löschst, wird der Timer zurückgesetzt und zählt ab dem nächsten Start neu.

## Anpassungen

Du kannst das Verhalten in der Datei `/usr/local/bin/screen_glitch.py` anpassen:

### Häufigkeit der Glitches ändern

Finde diese Zeile (ca. Zeile 102):

```python
wait_time = random.uniform(3.0, 10.0)
```

- Erste Zahl = minimale Pause zwischen Glitches (in Sekunden)
- Zweite Zahl = maximale Pause

**Beispiel:** Für häufigere Glitches (alle 1-5 Sekunden):

```python
wait_time = random.uniform(1.0, 5.0)
```

### Dauer der Glitches ändern

Finde diese Zeile (ca. Zeile 111):

```python
glitch_duration = random.uniform(0.05, 0.3)
```

- Erste Zahl = minimale Glitch-Dauer (in Sekunden)
- Zweite Zahl = maximale Glitch-Dauer

**Beispiel:** Für längere Glitches:

```python
glitch_duration = random.uniform(0.2, 0.8)
```

### Intensität der Verschiebung ändern

Finde die `offsets` in der `apply_glitch` Methode (ca. Zeile 31):

```python
offsets = {
    'low': (1, 2),
    'medium': (2, 4),
    'high': (3, 6)
}
```

Die Zahlen sind (x_offset, y_offset) in Pixeln. Größere Werte = stärkeres Zittern.

**Nach Änderungen:** Service neu starten:

```bash
sudo systemctl restart screen-glitch
```

## Deinstallation

### Automatisch

Das Programm löscht sich nach 30 Tagen automatisch. Es sind keine manuellen Schritte notwendig.

### Manuell (vor Ablauf der 30 Tage)

Wenn du das Programm vorzeitig entfernen möchtest:

```bash
sudo systemctl stop screen-glitch
sudo systemctl disable screen-glitch
sudo rm /etc/systemd/system/screen-glitch.service
sudo rm /usr/local/bin/screen_glitch.py
sudo rm /var/lib/screen-glitch-timestamp.json
sudo systemctl daemon-reload
```

## Anforderungen

- Raspberry Pi OS mit Desktop-Umgebung
- X11 (Standard bei Raspberry Pi OS Desktop)
- Python 3 (vorinstalliert)
- `xrandr` (vorinstalliert)

## Hinweise

- Das Programm verwendet `xrandr` für die visuellen Effekte
- Es läuft als systemd Service im Hintergrund
- Der Effekt startet automatisch nach dem Booten
- Die Effekte sind temporär und beschädigen nichts

## Fehlerbehebung

**Service startet nicht:**

```bash
sudo journalctl -u screen-glitch -n 50
```

**Display-Name finden:**

```bash
xrandr
```

**Manuell testen (ohne Service):**

```bash
python3 screen_glitch.py
```

## Technische Details

Das Programm nutzt:

- **xrandr –panning** für den Zitter-Effekt
- **xrandr –gamma** für die Farbverschiebung (chromatische Aberration)
- **systemd** für Autostart und Hintergrund-Ausführung
- **JSON-Timestamp-Datei** für die Selbstzerstörung nach 30 Tagen

### Selbstzerstörungs-Mechanismus

1. Beim ersten Start wird ein Timestamp in `/var/lib/screen-glitch-timestamp.json` gespeichert
1. Bei jedem Programmstart und in der Hauptschleife wird geprüft, ob 30 Tage vergangen sind
1. Wenn das Ablaufdatum erreicht ist:
- Service wird gestoppt und deaktiviert
- Service-Datei wird gelöscht
- Hauptprogramm wird gelöscht
- Timestamp-Datei wird gelöscht
- systemd wird neu geladen
1. Das Programm beendet sich selbst

Die Prüfung erfolgt kontinuierlich, sodass die Löschung innerhalb weniger Sekunden nach Ablauf der 30 Tage erfolgt.
