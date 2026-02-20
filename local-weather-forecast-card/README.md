# Local Weather Forecast Card (HACS Dashboard)

Custom Lovelace card for the **Local Weather Forecast** integration.

## Features
- Clear 3-block layout: now / next slot / later slot
- Forecast text, pressure trend and rain probabilities
- Defensive rendering when entities are unavailable at startup
- Language labels derived from integration language index
- Polished visual style (gradients + card sections)

## Requirements
- Home Assistant
- Integration sensors:
  - `sensor.local_forecast`
  - `sensor.local_forecast_zambretti_detail`
  - `sensor.local_forecast_pressurechange`

## Installation with HACS
1. HACS → menu (⋮) → **Custom repositories**.
2. Add this repository URL.
3. Category: **Dashboard** (backend HACS: plugin).
4. Install **Local Weather Forecast Card**.
5. Reload browser cache.

## Card configuration

```yaml
type: custom:local-weather-forecast-card
entity: sensor.local_forecast
detail_entity: sensor.local_forecast_zambretti_detail
pressure_change_entity: sensor.local_forecast_pressurechange
```

## Optional configuration

```yaml
type: custom:local-weather-forecast-card
entity: sensor.local_forecast
detail_entity: sensor.local_forecast_zambretti_detail
pressure_change_entity: sensor.local_forecast_pressurechange
icon_now: mdi:weather-cloudy-clock
```

## Notes
- This card is read-only and displays values produced by the integration.
- Missing values are rendered as `-` until sensors are available.

---

# Version Française

Carte Lovelace custom pour l’intégration **Local Weather Forecast**.

## Fonctionnalités
- Mise en page claire en 3 blocs : maintenant / prochain créneau / créneau suivant
- Texte de prévision, tendance de pression et probabilités de pluie
- Rendu robuste quand les entités sont indisponibles au démarrage
- Libellés de langue basés sur l’index de langue de l’intégration
- Style visuel amélioré (dégradés + sections de carte)

## Prérequis
- Home Assistant
- Capteurs de l’intégration :
  - `sensor.local_forecast`
  - `sensor.local_forecast_zambretti_detail`
  - `sensor.local_forecast_pressurechange`

## Installation via HACS
1. HACS → menu (⋮) → **Dépôts personnalisés**.
2. Ajoutez l’URL de ce dépôt.
3. Catégorie : **Dashboard** (backend HACS : plugin).
4. Installez **Local Weather Forecast Card**.
5. Rechargez le cache du navigateur.

## Configuration de la carte

```yaml
type: custom:local-weather-forecast-card
entity: sensor.local_forecast
detail_entity: sensor.local_forecast_zambretti_detail
pressure_change_entity: sensor.local_forecast_pressurechange
```

## Configuration optionnelle

```yaml
type: custom:local-weather-forecast-card
entity: sensor.local_forecast
detail_entity: sensor.local_forecast_zambretti_detail
pressure_change_entity: sensor.local_forecast_pressurechange
icon_now: mdi:weather-cloudy-clock
```

## Notes
- Cette carte est en lecture seule et affiche les valeurs produites par l’intégration.
- Les valeurs manquantes sont affichées par `-` tant que les capteurs ne sont pas disponibles.
