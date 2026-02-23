# Barocast HA (Local Weather Forecast Integration)

Repository: `barocast-ha`

Local weather forecast for Home Assistant based on pressure trend algorithms (Zambretti + Negretti/Zambra).

This repository contains only the HACS custom integration:
- `custom_components/local_weather_forecast/`

Related dashboard card repository:
- https://github.com/lennvilardi/barocast-ha-card

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

## Algorithm references
- https://github.com/sassoftware/iot-zambretti-weather-forcasting
- https://integritext.net/DrKFS/zambretti.htm
- https://www.mikrocontroller.net/topic/385242
- http://www.beteljuice.co.uk/zambretti/forecast.html

## Development notes
- Validation workflows are included for HACS + hassfest + gitleaks.
- `GITHUB_PUBLISH.md` contains publication instructions for this integration repository.

---

# Version Française

Prévision météo locale pour Home Assistant basée sur les tendances de pression (Zambretti + Negretti/Zambra).

Ce dépôt contient uniquement l’intégration HACS :
- `custom_components/local_weather_forecast/`

Dépôt de la carte dashboard associé :
- https://github.com/lennvilardi/barocast-ha-card

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

## Références algorithmiques
- https://github.com/sassoftware/iot-zambretti-weather-forcasting
- https://integritext.net/DrKFS/zambretti.htm
- https://www.mikrocontroller.net/topic/385242
- http://www.beteljuice.co.uk/zambretti/forecast.html

## Notes de développement
- Workflows de validation inclus : HACS + hassfest + gitleaks.
- `GITHUB_PUBLISH.md` contient la procédure de publication pour ce dépôt d’intégration.
