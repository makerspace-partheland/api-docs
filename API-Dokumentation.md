# Makerspace Partheland - Sensordaten API

Diese Dokumentation beschreibt, wie Sie die Sensordaten des Makerspace Partheland in Ihre eigenen Anwendungen einbinden können.

## Inhaltsverzeichnis
- [Übersicht](#übersicht)
- [Verfügbare Daten](#verfügbare-daten)
- [Zugriffsmöglichkeiten](#zugriffsmöglichkeiten)
- [Anwendungsbeispiele](#anwendungsbeispiele)
- [Anwendungsideen für Wasserstandsdaten](#anwendungsideen-für-wasserstandsdaten)
- [Technische Details](#technische-details)

## Übersicht

Der Makerspace Partheland stellt Umwelt- und Sensordaten öffentlich zur Verfügung. Diese Daten können Sie für verschiedene Zwecke nutzen:
- 🏠 Smart Home Automation
- 🏫 Bildungsprojekte
- �� Umweltmonitoring
- 💧 Gewässerüberwachung
- 📊 Datenanalyse

## Verfügbare Daten

### SenseBox Messstationen
Unsere SenseBox:home Stationen messen:
- 🌡️ Temperatur (in °C)
- 💧 Luftfeuchtigkeit (in %)
- 📊 Luftdruck (in hPa)
- 💨 Feinstaub (PM10 und PM2.5)
- 🔆 UV-Intensität
- 💡 Beleuchtungsstärke
- 🔊 Lautstärke (in dB)

### Wasserstandssensoren
Die Wasserstandssensoren erfassen:
- 💧 Wasserstand (in cm)
- 📊 Pegeltrends
- 🔋 Batteriestatus
- 📏 Messdistanz

## Zugriffsmöglichkeiten

### 1. Echtzeit-Updates via MQTT (WebSocket)
Ideal für:
- Smart Home Systeme (Home Assistant, ioBroker, etc.)
- Live-Anzeigen
- Automatisierungen

**Verbindungsdaten:**
```
URL: wss://mqtt.makerspace-partheland.de:443/mqtt
```

**Topics für SenseBox Daten:**
```
senseBox:home/Beucha_Nr1
```

Beispiel-Nachricht:
```json
{
  "fields": {
    "Temperatur": 7.9,
    "Luftfeuchte": 84.3,
    "Luftdruck": 995.2,
    "PM10": 38.2,
    "PM2.5": 17.9,
    "UV-Intensitaet": 0,
    "Beleuchtungsstaerke": 0,
    "Lautstaerke": 45.2
  },
  "name": "Beucha_Nr1",
  "timestamp": 1743194885
}
```

**Topics für Wasserstandsdaten:**
```
sensoren/LDDS75_Naunhof_1
```

Beispiel-Nachricht:
```json
{
  "fields": {
    "water_level": 327,
    "meldestufe": 0,
    "water": "Parthe",
    "bat": 3.264
  },
  "name": "LDDS75_Naunhof_1",
  "timestamp": 1743193867
}
```

### 2. REST-API
Ideal für:
- Webseiten
- Apps
- Datenanalyse
- Historische Daten

**Basis-URL:**
```
https://data.makerspace-partheland.de/
```

**Endpunkte:**
- Alle SenseBox Daten: `/v1/LoRaDevices/senseboxes`
- Spezifische SenseBox: `/v1/LoRaDevices/senseboxes?device=Beucha_Nr1`
- Alle Wasserstände: `/v1/LoRaDevices/waterlevels`
- Spezifischer Wasserstand: `/v1/LoRaDevices/waterlevels?device=LDDS75_Naunhof_1`

## Anwendungsbeispiele

### 1a. Home Assistant Integration
```yaml
mqtt:
  sensor:
    - name: "Außentemperatur Beucha"
      state_topic: "senseBox:home/Beucha_Nr1"
      value_template: "{{ value_json.fields.Temperatur }}"
      unit_of_measurement: "°C"
    
    - name: "Luftqualität PM10"
      state_topic: "senseBox:home/Beucha_Nr1"
      value_template: "{{ value_json.fields.PM10 }}"
      unit_of_measurement: "µg/m³"

    - name: "Wasserstand Parthe"
      state_topic: "sensoren/LDDS75_Naunhof_1"
      value_template: "{{ value_json.fields.water_level }}"
      unit_of_measurement: "cm"
```

Diese Home Assistant Konfiguration:
1. Erstellt drei MQTT-Sensoren für verschiedene Messwerte
2. Nutzt die MQTT-Integration von Home Assistant
3. Extrahiert die Werte mittels value_template aus den JSON-Nachrichten
4. Definiert passende Einheiten für die Anzeige

Sie können die Konfiguration erweitern durch:
- Hinzufügen weiterer Sensoren (z.B. Luftfeuchte, UV-Intensität)
- Erstellen von Automationen basierend auf den Werten
- Einbinden in Dashboards und Grafiken
- Konfigurieren von Grenzwert-Benachrichtigungen

### 1b. ioBroker Integration
Für die Integration in ioBroker benötigen Sie den MQTT-Adapter. Hier ein Beispiel für die Konfiguration:

1. MQTT-Adapter Installation und Konfiguration:
```yaml
Instanz-Einstellungen:
  URL: wss://mqtt.makerspace-partheland.de:443/mqtt
  Websoket: aktiviert
  SSL: aktiviert
  Port: 443
  Path: /mqtt
```

2. MQTT-Subscriptions in der Adapter-Konfiguration:
```
senseBox:home/Beucha_Nr1
sensoren/LDDS75_Naunhof_1
```

3. Beispiel JavaScript für die Datenverarbeitung (Script-Adapter):
```javascript
// Überwachung der Sensordaten
on({id: 'mqtt.0.senseBox:home.Beucha_Nr1'}, (obj) => {
    try {
        const data = JSON.parse(obj.state.val);
        
        // Erstelle/Aktualisiere Datenpunkte
        setState('javascript.0.sensoren.beucha.temperatur', {
            val: data.fields.Temperatur,
            ack: true,
            unit: '°C'
        });
        
        setState('javascript.0.sensoren.beucha.luftfeuchte', {
            val: data.fields.Luftfeuchte,
            ack: true,
            unit: '%'
        });
        
        // Berechne Taupunkt
        const taupunkt = taupunktBerechnung(data.fields.Temperatur, data.fields.Luftfeuchte);
        setState('javascript.0.sensoren.beucha.taupunkt', {
            val: taupunkt,
            ack: true,
            unit: '°C'
        });
        
    } catch (e) {
        console.error('Fehler bei der Verarbeitung der SenseBox-Daten: ' + e);
    }
});

// Überwachung der Wasserstandsdaten
on({id: 'mqtt.0.sensoren.LDDS75_Naunhof_1'}, (obj) => {
    try {
        const data = JSON.parse(obj.state.val);
        
        setState('javascript.0.sensoren.parthe.wasserstand', {
            val: data.fields.water_level,
            ack: true,
            unit: 'cm'
        });
        
        // Batteriewarnung bei niedrigem Stand
        if (data.fields.bat < 3.3) {
            sendTo('telegram.0', {
                text: `⚠️ Batterie niedrig bei ${data.name}: ${data.fields.bat}V`
            });
        }
        
    } catch (e) {
        console.error('Fehler bei der Verarbeitung der Wasserstandsdaten: ' + e);
    }
});

// Hilfsfunktion zur Taupunktberechnung
function taupunktBerechnung(temp, humidity) {
    const a = 17.27;
    const b = 237.7;
    const alpha = ((a * temp) / (b + temp)) + Math.log(humidity/100);
    return (b * alpha) / (a - alpha);
}
```

4. Beispiel für eine VIS-Ansicht:
```javascript
[{"tpl":"tplValueFloat","data":{"oid":"javascript.0.sensoren.beucha.temperatur","visibility-cond":"==","visibility-val":1,"is_comma":true,"factor":1,"digits":1,"append":"°C","prepend":"Temperatur: "}},
 {"tpl":"tplValueFloat","data":{"oid":"javascript.0.sensoren.beucha.luftfeuchte","visibility-cond":"==","visibility-val":1,"is_comma":true,"factor":1,"digits":1,"append":"%","prepend":"Luftfeuchte: "}},
 {"tpl":"tplValueFloat","data":{"oid":"javascript.0.sensoren.parthe.wasserstand","visibility-cond":"==","visibility-val":1,"is_comma":true,"factor":1,"digits":0,"append":"cm","prepend":"Wasserstand: "}}]
```

Dieses ioBroker-Setup bietet:
1. Automatische MQTT-Verbindung über WebSocket
2. Strukturierte Datenpunkte für alle Sensormesswerte
3. Berechnete Werte (z.B. Taupunkt)
4. Batterieüberwachung mit Telegram-Benachrichtigung
5. Fertige VIS-Widgets zur Anzeige

Sie können die Integration erweitern durch:
- Erstellen von Blockly-Programmen für weitere Automatisierungen
- Hinzufügen von Grenzwertalarmen
- Integration in Flot oder Echarts Grafiken
- Verknüpfung mit anderen Adaptern (z.B. Wettervorhersage)
- Erstellung eigener VIS-Widgets
- Export der Daten in Influx/SQL-Datenbanken

### 2. Node-RED Flow für Gewässermonitoring
```json
[
    {
        "id": "mqtt-in",
        "type": "mqtt in",
        "topic": "sensoren/LDDS75_Naunhof_1",
        "mqtt": {
            "server": "wss://mqtt.makerspace-partheland.de:443/mqtt"
        },
        "wires": [["json-parse"]]
    },
    {
        "id": "json-parse",
        "type": "json",
        "wires": [["store-data"]]
    },
    {
        "id": "store-data",
        "type": "function",
        "name": "Speichere Messwerte",
        "func": "// Speichere die letzten 12 Messwerte (2 Stunden)\nconst maxLength = 12;\n\n// Hole gespeicherte Werte oder initialisiere Array\nflow.measurements = flow.measurements || [];\n\n// Füge neuen Messwert hinzu\nflow.measurements.push({\n    timestamp: Date.now(),\n    value: msg.payload.fields.water_level\n});\n\n// Behalte nur die letzten X Messungen\nif (flow.measurements.length > maxLength) {\n    flow.measurements.shift();\n}\n\n// Berechne Trend\nif (flow.measurements.length >= 2) {\n    const oldest = flow.measurements[0].value;\n    const newest = flow.measurements[flow.measurements.length - 1].value;\n    const trend = newest - oldest;\n    \n    msg.trend = trend;\n    msg.trendPercent = (trend / oldest * 100).toFixed(1);\n    msg.currentValue = newest;\n    \n    return msg;\n}\n\nreturn null;",
        "wires": [["check-trend"]]
    },
    {
        "id": "check-trend",
        "type": "switch",
        "name": "Prüfe Trend",
        "rules": [
            {
                "t": "gt",
                "v": "5",
                "vt": "num"
            },
            {
                "t": "lt",
                "v": "-5",
                "vt": "num"
            }
        ],
        "wires": [["create-message"], ["create-message"]]
    },
    {
        "id": "create-message",
        "type": "template",
        "name": "Erstelle Nachricht",
        "template": "Wasserstandsänderung: {{ payload.trendPercent }}%\nAktueller Stand: {{ payload.currentValue }} cm",
        "wires": [["notify"]]
    },
    {
        "id": "notify",
        "type": "debug",
        "name": "Ausgabe",
        "active": true,
        "complete": "payload"
    }
]
```

Dieser Flow:
1. Empfängt MQTT-Nachrichten vom Wasserstandssensor
2. Wandelt die JSON-Daten in ein Objekt um
3. Speichert die letzten 12 Messwerte (2 Stunden bei 10-Minuten-Intervallen)
4. Berechnet den Trend über diesen Zeitraum
5. Benachrichtigt bei Änderungen über 5% (kann an Debug-Node oder Benachrichtigungsdienst angeschlossen werden)

Sie können den Flow anpassen durch:
- Ändern der `maxLength` für längere/kürzere Beobachtungszeiträume
- Anpassen der Schwellwerte in der Switch-Node (aktuell 5/-5)
- Ersetzen der Debug-Node durch Email, Telegram, Push-Benachrichtigungen etc.

### 3. Python-Script für Gewässeranalyse
```python
import requests
import pandas as pd
from datetime import datetime, timedelta

# Abruf der Wasserstandsdaten
response = requests.get('https://data.makerspace-partheland.de/v1/LoRaDevices/waterlevels?device=LDDS75_Naunhof_1')
data = response.json()

# Daten in DataFrame umwandeln
df = pd.DataFrame({
    'Wasserstand': [data['features'][0]['properties']['fields']['water_level']],
    'Zeitstempel': [datetime.fromtimestamp(data['features'][0]['properties']['lastSeen'])],
    'Gewässer': [data['features'][0]['properties']['fields']['water']]
})

# Analyse
print(f"Aktueller Wasserstand {df['Gewässer'][0]}: {df['Wasserstand'][0]} cm")
print(f"Letzte Messung: {df['Zeitstempel'][0].strftime('%d.%m.%Y %H:%M')}")
```

Dieses Python-Script:
1. Nutzt die REST-API zum Abrufen der Wasserstandsdaten
2. Konvertiert die Unix-Timestamps in lesbare Zeitstempel
3. Strukturiert die Daten in einem Pandas DataFrame für weitere Analysen
4. Gibt eine formatierte Zusammenfassung aus

Sie können das Script erweitern durch:
- Abrufen historischer Daten für Trendanalysen
- Erstellen von Matplotlib/Seaborn Visualisierungen
- Export der Daten in CSV/Excel für weitere Verarbeitung
- Implementierung von statistischen Analysen
- Kombination mit Wetterdaten für Korrelationsanalysen

### 4. Schulprojekt: Gewässerökologie
```javascript
// HTML + Chart.js
const ctx = document.getElementById('wasserstandChart').getContext('2d');
const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Wasserstand Parthe',
            data: [],
            borderColor: 'rgb(54, 162, 235)',
            tension: 0.1
        }]
    },
    options: {
        scales: {
            y: {
                title: {
                    display: true,
                    text: 'Wasserstand (cm)'
                }
            }
        }
    }
});

// MQTT Verbindung
const client = mqtt.connect('wss://mqtt.makerspace-partheland.de:443/mqtt');
client.subscribe('sensoren/LDDS75_Naunhof_1');

client.on('message', (topic, message) => {
    const data = JSON.parse(message);
    const zeit = new Date().toLocaleTimeString();
    
    // Füge neue Daten hinzu
    chart.data.labels.push(zeit);
    chart.data.datasets[0].data.push(data.fields.water_level);
    
    // Behalte nur die letzten 24 Stunden
    if (chart.data.labels.length > 288) { // 24h * 12 Messungen/Stunde
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
    }
    
    chart.update();
});
```

Dieses JavaScript-Beispiel:
1. Erstellt ein interaktives Liniendiagramm mit Chart.js
2. Verbindet sich über WebSocket mit dem MQTT-Broker
3. Aktualisiert das Diagramm in Echtzeit mit neuen Messwerten
4. Behält einen 24-Stunden-Verlauf bei (288 Messpunkte)
5. Formatiert die Zeitachse automatisch

Sie können das Beispiel erweitern durch:
- Hinzufügen mehrerer Datensätze (z.B. verschiedene Messstellen)
- Implementierung von Zoom- und Pan-Funktionen
- Export der Daten als CSV oder Bild
- Anzeige von Minimum/Maximum/Durchschnittswerten
- Hinzufügen von Schwellwert-Markierungen
- Integration in eine größere Webapplikation

Benötigte HTML-Struktur:
```html
<canvas id="wasserstandChart"></canvas>

<!-- Erforderliche Bibliotheken -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>
```

## Anwendungsideen für Wasserstandsdaten

### Umweltbildung
- 📚 Langzeitbeobachtung von Gewässern
- 🌱 Zusammenhang zwischen Niederschlag und Wasserstand
- 🔍 Einfluss der Jahreszeiten auf Gewässer

### Gewässermanagement
- 📊 Pegelstandsüberwachung
- 💧 Wasserressourcenmanagement
- 🌿 Ökologische Durchgängigkeit

### Freizeitaktivitäten
- 🚣 Wassersport (Kanu, Rudern)
- 🎣 Angelsport
- 🏊 Badegewässer

### Wissenschaft & Forschung
- 📈 Langzeitstudien
- 🌍 Klimawandelauswirkungen
- 💧 Grundwasserspiegel-Korrelation

## Technische Details

### Datenaktualisierung
- SenseBox Daten: Alle 1-5 Minuten
- Wasserstandsdaten: Alle 15-30 Minuten

### Datenformate
- Alle Zeitstempel sind Unix-Timestamps (Sekunden seit 1970)
- Temperatur in °C
- Luftfeuchte in %
- Luftdruck in hPa
- Feinstaub in µg/m³
- Wasserstand in cm
- UV-Intensität in mW/m²
- Lautstärke in dB

### Fehlerbehebung
1. Keine MQTT-Verbindung:
   - Überprüfen Sie die WebSocket-URL
   - Stellen Sie sicher, dass SSL/TLS aktiviert ist

2. Keine Daten:
   - Überprüfen Sie das Topic-Format
   - Prüfen Sie die Zeitstempel der letzten Nachricht