# LoRa Geräte API

Eine RESTful API für den Zugriff auf LoRa-Geräte und deren Sensordaten des Makerspace Partheland e.V.

## Übersicht

Diese API ermöglicht den Zugriff auf Daten von verschiedenen LoRa-Geräten, darunter senseBoxen und Wasserstandssensoren. Sie bietet Endpunkte zum Abrufen von Geräteinformationen, Statusabfragen und detaillierten Sensordaten.

## API-Basis-URL
https://data.makerspace-partheland.de/v1

## Authentifizierung

Einige Endpunkte erfordern eine Authentifizierung mittels API-Key. Der API-Key muss im Header der Anfrage als `x-api-key` übermittelt werden.


## Hauptendpunkte

- `/LoRaDevices` - Liste aller LoRa-Geräte (öffentlich zugänglich)
- `/LoRaDevices/senseboxes` - Liste aller senseBox-Geräte (öffentlich zugänglich)
- `/LoRaDevices/waterlevels` - Liste aller Wasserstand/Pegelstands-Geräte (öffentlich zugänglich)
- `/v2/ingest` - HTTP-Upload für externe Messdatenzulieferer (erfordert API-Key)

Jeder Gerätetyp bietet zusätzliche Endpunkte:

- `/{gerätetyp}/health` - Statusabfrage der Geräte (öffentlich zugänglich)
- `/{gerätetyp}/details` - Detaillierte Informationen und Sensorenwerte zu einem bestimmten Gerät (erfordert API-Key)

## Beispielanfragen

### Alle LoRa-Geräte abrufe

```bash
curl -X GET "https://data.makerspace-partheland.de/v1/LoRaDevices"
```

### Status einer bestimmten senseBox abrufen

```bash
curl -X GET "https://data.makerspace-partheland.de/v1/LoRaDevices/senseboxes/details?name=Beucha_Nr1"
```

### Status einer bestimmten Wasserstand/Pegelstands-Gerät abrufen

```bash
curl -X GET "https://data.makerspace-partheland.de/v1/LoRaDevices/waterlevels/details?name=LDDS75_Naunhof_1"
```

### Messdaten hochladen

```bash
curl -X POST "https://data.makerspace-partheland.de/v2/ingest" \
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

Bei Fragen oder Problemen melde Dich bitte via: https://makerspace-partheland.de/austausch/
