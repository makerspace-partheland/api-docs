# Sensordaten API

Diese Dokumentation beschreibt die öffentliche Sensordaten-API des Makerspace Partheland e.V.

## Basis

```text
https://data.makerspace-partheland.de
```

Die API liefert aktuelle Geräte-, Gateway- und Sensordaten. Die Ausgaben stehen als GeoJSON oder NGSI-LD bereit.

Einige Detail- und Upload-Funktionen benötigen einen API-Key im Header:

```text
x-api-key: DEIN_API_KEY
```

Upload-Keys werden nicht öffentlich ausgegeben. Kontakt: https://makerspace-partheland.de/austausch/

## Endpunkte

| Methode | Pfad | Inhalt |
|---|---|---|
| `GET` | `/geojson/devices` | Alle Geräte als GeoJSON |
| `GET` | `/geojson/devices/{type}` | Geräte eines Typs als GeoJSON |
| `GET` | `/geojson/devices/{type}/{id}` | Einzelnes Gerät als GeoJSON |
| `GET` | `/ngsi-ld/entities` | Alle Geräte als NGSI-LD |
| `GET` | `/ngsi-ld/entities/{type}` | Geräte eines Typs als NGSI-LD |
| `GET` | `/ngsi-ld/entities/{type}/{id}` | Einzelnes Gerät als NGSI-LD |
| `GET` | `/geojson/gateways` | Alle Gateways als GeoJSON |
| `GET` | `/geojson/gateways/{id}` | Einzelnes Gateway als GeoJSON |
| `POST` | `/ingest` | Messdaten hochladen |

Gültige Gerätetypen:

```text
sensebox
waterlevel
temperature
moisture
```

## Geräte als GeoJSON

Alle Geräte:

```bash
curl -X GET "https://data.makerspace-partheland.de/geojson/devices"
```

Geräte nach Typ:

```bash
curl -X GET "https://data.makerspace-partheland.de/geojson/devices/waterlevel"
```

Bodenfeuchte-Geräte:

```bash
curl -X GET "https://data.makerspace-partheland.de/geojson/devices/moisture"
```

Ein einzelnes Gerät:

```bash
curl -X GET "https://data.makerspace-partheland.de/geojson/devices/sensebox/mspl-70b3d57ed004ce79"
```

Die Antwort ist eine GeoJSON-`FeatureCollection`. Messwerte stehen unter `properties.measurements`.

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": "eui-a84041603a5a0171",
      "geometry": {
        "type": "Point",
        "coordinates": [12.50305, 51.26937]
      },
      "properties": {
        "name": "LDDS75 Großpösna 2",
        "type": "WaterLevelDevice",
        "status": "online",
        "last_seen": "2026-07-02T07:30:24.738Z",
        "measurements": {
          "water_level": {
            "value": 28,
            "unit": "MMT",
            "timestamp": "2026-07-02T07:30:24.738Z"
          }
        }
      }
    }
  ]
}
```

## Geräte als NGSI-LD

Alle Geräte:

```bash
curl -X GET "https://data.makerspace-partheland.de/ngsi-ld/entities"
```

Geräte nach Typ:

```bash
curl -X GET "https://data.makerspace-partheland.de/ngsi-ld/entities/sensebox"
```

Bodenfeuchte-Geräte:

```bash
curl -X GET "https://data.makerspace-partheland.de/ngsi-ld/entities/moisture"
```

Ein einzelnes Gerät:

```bash
curl -X GET "https://data.makerspace-partheland.de/ngsi-ld/entities/sensebox/mspl-70b3d57ed004ce79"
```

NGSI-LD-Antworten enthalten `id`, `type`, Eigenschaften als `Property` oder `GeoProperty` und den NGSI-LD-Kontext.

## Gateways

Alle Gateways:

```bash
curl -X GET "https://data.makerspace-partheland.de/geojson/gateways"
```

Ein einzelnes Gateway:

```bash
curl -X GET "https://data.makerspace-partheland.de/geojson/gateways/db-ware-gateway-dreimu-001"
```

Gateway-Antworten sind GeoJSON-`FeatureCollection`-Objekte.

## Messdaten hochladen

Externe Zulieferer können Messdaten per HTTP hochladen. Die Payload wird vor der Anbindung abgestimmt. Die maximale Payload-Größe beträgt 64 KiB.

```bash
curl -X POST "https://data.makerspace-partheland.de/ingest" \
  -H "x-api-key: DEIN_UPLOAD_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "deviceInfo": {
      "deviceName": "test-device-001"
    },
    "time": "2026-05-08T21:40:00Z",
    "object": {
      "temperature": 21.4,
      "humidity": 55
    }
  }'
```

Erfolgreiche Uploads werden mit `202 Accepted` angenommen:

```json
{
  "id": "1778276243090-6a1884aa42553",
  "status": "accepted"
}
```

## MQTT

Zusätzlich zur REST-API stehen aktuelle Messwerte per MQTT über WebSocket bereit:

```text
wss://mqtt.makerspace-partheland.de:443/mqtt
```

Beispiel-Topics:

```text
senseBox:home/Beucha_Nr1
sensoren/LDDS75_Naunhof_1
```

## OpenAPI

Die OpenAPI-Spezifikation liegt in `swagger.yaml`. Die gerenderte Swagger-UI ist unter https://api-docs.makerspace-partheland.de/ erreichbar.
