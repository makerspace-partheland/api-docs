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

### 1. Home Assistant Integration
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

### 2. Node-RED Flow für Gewässermonitoring
```json
[
  {
    "id": "wasserstand",
    "type": "mqtt in",
    "topic": "sensoren/LDDS75_Naunhof_1",
    "mqtt": {
      "server": "wss://mqtt.makerspace-partheland.de:443/mqtt"
    }
  },
  {
    "id": "analyse",
    "type": "function",
    "func": "// Berechne Trend über die letzten Stunden\nlet trend = calculateTrend(msg.payload.fields.water_level);\nif (Math.abs(trend) > 5) return msg;",
    "wires": [["notify"]]
  }
]
```

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