# Sensordaten API

Eine RESTful API für den Zugriff auf Geräte, Gateways und Sensordaten des Makerspace Partheland e.V.

## Übersicht

Diese API ermöglicht den Zugriff auf aktuelle Geräte-, Gateway- und Sensordaten. Die öffentlichen Daten stehen als GeoJSON und NGSI-LD bereit.

## API-Basis-URL
https://data.makerspace-partheland.de

## Authentifizierung

Einige Endpunkte erfordern eine Authentifizierung mittels API-Key. Der API-Key muss im Header der Anfrage als `x-api-key` übermittelt werden.


## Hauptendpunkte

- `/geojson/devices` - Geräte und Sensordaten als GeoJSON
- `/geojson/devices/{type}` - Geräte nach Typ als GeoJSON
- `/geojson/devices/{type}/{id}` - Einzelnes Gerät als GeoJSON
- `/ngsi-ld/entities` - Geräte und Sensordaten als NGSI-LD
- `/ngsi-ld/entities/{type}` - Geräte nach Typ als NGSI-LD
- `/ngsi-ld/entities/{type}/{id}` - Einzelnes Gerät als NGSI-LD
- `/geojson/gateways` - Gateways als GeoJSON
- `/geojson/gateways/{id}` - Einzelnes Gateway als GeoJSON
- `/ingest` - HTTP-Upload für externe Messdatenzulieferer (erfordert API-Key)

Gängige Gerätetypen sind `sensebox`, `waterlevel`, `temperature` und `moisture`.

## Beispielanfragen

### Alle Geräte als GeoJSON abrufen

```bash
curl -X GET "https://data.makerspace-partheland.de/geojson/devices"
```

### Geräte eines Typs als GeoJSON abrufen

```bash
curl -X GET "https://data.makerspace-partheland.de/geojson/devices/sensebox"
```

### Geräte als NGSI-LD abrufen

```bash
curl -X GET "https://data.makerspace-partheland.de/ngsi-ld/entities"
```

### Gateways als GeoJSON abrufen

```bash
curl -X GET "https://data.makerspace-partheland.de/geojson/gateways"
```

### Messdaten hochladen

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

Upload-Keys werden nicht öffentlich ausgegeben. Für einen Key bitte über https://makerspace-partheland.de/austausch/ Kontakt aufnehmen.

## Dokumentation

Die vollständige API-Dokumentation ist als OpenAPI (Swagger) Spezifikation verfügbar:

- [OpenAPI Dokumentation](https://data.makerspace-partheland.de/swagger)

## Wartung

Swagger UI und GitHub-Actions-Abhängigkeiten werden automatisiert aktualisiert. Die daraus entstehenden PRs werden nach den normalen GitHub-Actions-Prüfungen übernommen; größere Versionswechsel werden getrennt geprüft.

## Unterstützung

Bei Fragen oder Problemen: https://makerspace-partheland.de/austausch/
