#!/bin/bash

# Installation Script für Screen Glitch Effect

echo “=== Screen Glitch Effect Installation ===”
echo “”

# Prüfe ob Script als root läuft

if [ “$EUID” -ne 0 ]; then
echo “Bitte als root ausführen (sudo ./install.sh)”
exit 1
fi

# Kopiere das Python-Script nach /usr/local/bin

echo “[1/5] Kopiere screen_glitch.py nach /usr/local/bin…”
cp screen_glitch.py /usr/local/bin/screen_glitch.py
chmod +x /usr/local/bin/screen_glitch.py

# Erstelle Verzeichnis für Timestamp-Datei

echo “[2/5] Erstelle Timestamp-Verzeichnis…”
mkdir -p /var/lib
chmod 755 /var/lib

# Erstelle systemd Service

echo “[3/5] Erstelle systemd Service…”
cat > /etc/systemd/system/screen-glitch.service << ‘EOF’
[Unit]
Description=Screen Glitch Effect
After=graphical.target

[Service]
Type=simple
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/pi/.Xauthority
ExecStart=/usr/bin/python3 /usr/local/bin/screen_glitch.py
Restart=on-failure
User=pi

[Install]
WantedBy=graphical.target
EOF

# Aktiviere und starte den Service

echo “[4/5] Aktiviere Service…”
systemctl daemon-reload
systemctl enable screen-glitch.service

echo “[5/5] Starte Service…”
systemctl start screen-glitch.service

echo “”
echo “=== Installation abgeschlossen! ===”
echo “”
echo “Der Screen Glitch Effect läuft jetzt im Hintergrund.”
echo “”
echo “⚠️  WICHTIG: Das Programm löscht sich automatisch nach genau 30 Tagen!”
echo “”
echo “Installationszeitpunkt wird in /var/lib/screen-glitch-timestamp.json gespeichert.”
echo “”
echo “Nützliche Befehle:”
echo “  Status prüfen:     sudo systemctl status screen-glitch”
echo “  Service stoppen:   sudo systemctl stop screen-glitch”
echo “  Service starten:   sudo systemctl start screen-glitch”
echo “  Autostart aus:     sudo systemctl disable screen-glitch”
echo “  Service entfernen: sudo systemctl stop screen-glitch && sudo systemctl disable screen-glitch”
echo “”
