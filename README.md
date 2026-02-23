# Barocast HA (Local Weather Forecast)

Repository: `barocast-ha`

Local weather forecast for Home Assistant based on pressure trend algorithms (Zambretti + Negretti/Zambra), with:
- a HACS custom integration (`local_weather_forecast`)
- a HACS dashboard card (`local-weather-forecast-card`)

## Repository layout
- `custom_components/local_weather_forecast/`: HACS integration (config flow + sensors)
- `local-weather-forecast-card/`: HACS dashboard card (custom Lovelace card)

## Quick start (Integration)
1. Add this repository to HACS as a **Custom repository** (type **Integration**).
2. Install **Local Weather Forecast**.
3. Restart Home Assistant.
4. Go to `Settings > Devices & Services > Add Integration`.
5. Configure:
   - language (`de`, `en`, `el`, `it`, `fr`)
   - pressure sensor (required)
   - temperature / wind speed / wind direction sensors (optional)
   - pressure sea-level mode, altitude, hemisphere, update interval

Created sensors:
- `sensor.local_forecast`
- `sensor.local_forecast_zambretti_detail`
- `sensor.local_forecast_neg_zam_detail`
- `sensor.local_forecast_pressure`
- `sensor.local_forecast_temperature`
- `sensor.local_forecast_pressurechange`
- `sensor.local_forecast_temperaturechange`

## Quick start (Dashboard card)
Use the dedicated folder/repo `local-weather-forecast-card/` in HACS as **Dashboard**.

Example Lovelace config:

```yaml
type: custom:local-weather-forecast-card
entity: sensor.local_forecast
detail_entity: sensor.local_forecast_zambretti_detail
pressure_change_entity: sensor.local_forecast_pressurechange
```

## Algorithm references
- https://github.com/sassoftware/iot-zambretti-weather-forcasting
- https://integritext.net/DrKFS/zambretti.htm
- https://www.mikrocontroller.net/topic/385242
- http://www.beteljuice.co.uk/zambretti/forecast.html

## Development notes
- Validation workflows are included for HACS + hassfest + gitleaks.
- `GITHUB_PUBLISH.md` contains step-by-step publication instructions for two separate GitHub repositories.

---

# Version Française

Prévision météo locale pour Home Assistant basée sur les tendances de pression (Zambretti + Negretti/Zambra), avec :
- une intégration HACS (`local_weather_forecast`)
- une carte dashboard HACS (`local-weather-forecast-card`)

## Structure du dépôt
- `custom_components/local_weather_forecast/` : intégration HACS (config flow + capteurs)
- `local-weather-forecast-card/` : carte dashboard HACS (carte Lovelace custom)

## Démarrage rapide (Intégration)
1. Ajoute ce dépôt dans HACS en **Custom repository** (type **Integration**).
2. Installe **Local Weather Forecast**.
3. Redémarre Home Assistant.
4. Va dans `Paramètres > Appareils et services > Ajouter une intégration`.
5. Configure :
   - langue (`de`, `en`, `el`, `it`, `fr`)
   - capteur de pression (obligatoire)
   - capteurs température / vitesse du vent / direction du vent (optionnels)
   - mode pression au niveau de la mer, altitude, hémisphère, intervalle de mise à jour

Capteurs créés :
- `sensor.local_forecast`
- `sensor.local_forecast_zambretti_detail`
- `sensor.local_forecast_neg_zam_detail`
- `sensor.local_forecast_pressure`
- `sensor.local_forecast_temperature`
- `sensor.local_forecast_pressurechange`
- `sensor.local_forecast_temperaturechange`

## Démarrage rapide (Carte dashboard)
Utilise le dossier/repo dédié `local-weather-forecast-card/` dans HACS en type **Dashboard**.

Exemple Lovelace :

```yaml
type: custom:local-weather-forecast-card
entity: sensor.local_forecast
detail_entity: sensor.local_forecast_zambretti_detail
pressure_change_entity: sensor.local_forecast_pressurechange
```

## Références algorithmiques
- https://github.com/sassoftware/iot-zambretti-weather-forcasting
- https://integritext.net/DrKFS/zambretti.htm
- https://www.mikrocontroller.net/topic/385242
- http://www.beteljuice.co.uk/zambretti/forecast.html

## Notes de développement
- Workflows de validation inclus : HACS + hassfest + gitleaks.
- `GITHUB_PUBLISH.md` contient la procédure de publication GitHub (2 dépôts séparés).
