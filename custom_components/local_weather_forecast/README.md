# Local Weather Forecast (HACS Integration)

A Home Assistant custom integration that computes a 12-hour local forecast from local sensors.

## What it does
- Implements Zambretti + Negretti/Zambra pressure-based forecast models.
- Provides forecast text, trend, rain probability proxies and icon hints.
- Exposes sensors compatible with legacy YAML cards.
- Adds a full Home Assistant config UI (config flow + options flow).

## Configuration UI
Required:
- Pressure sensor entity

Optional:
- Temperature sensor entity
- Wind speed sensor entity
- Wind direction sensor entity

Other options:
- Language (`de`, `en`, `el`, `it`, `fr`)
- Pressure is already sea-level corrected
- Altitude (meters)
- Hemisphere (north/south)
- Update interval (seconds)

## Exposed sensors
- `sensor.local_forecast`
- `sensor.local_forecast_zambretti_detail`
- `sensor.local_forecast_neg_zam_detail`
- `sensor.local_forecast_pressure`
- `sensor.local_forecast_temperature`
- `sensor.local_forecast_pressurechange`
- `sensor.local_forecast_temperaturechange`

## Compatibility notes
- Sensor names/attributes are intentionally close to the original YAML package.
- The integration keeps card compatibility while replacing template/statistics dependencies.

---

# Version Française

Intégration custom Home Assistant qui calcule une prévision locale 12h à partir de capteurs locaux.

## Ce que fait l'intégration
- Implémente les modèles de prévision basés sur la pression : Zambretti + Negretti/Zambra.
- Fournit texte de prévision, tendance, proxy de probabilité de pluie et icônes.
- Expose des capteurs compatibles avec les anciennes cartes YAML.
- Ajoute une configuration complète via l'interface Home Assistant (config flow + options flow).

## Interface de configuration
Obligatoire :
- Entité capteur de pression

Optionnel :
- Entité capteur de température
- Entité capteur de vitesse du vent
- Entité capteur de direction du vent

Autres options :
- Langue (`de`, `en`, `el`, `it`, `fr`)
- Pression déjà corrigée au niveau de la mer
- Altitude (mètres)
- Hémisphère (nord/sud)
- Intervalle de mise à jour (secondes)

## Capteurs exposés
- `sensor.local_forecast`
- `sensor.local_forecast_zambretti_detail`
- `sensor.local_forecast_neg_zam_detail`
- `sensor.local_forecast_pressure`
- `sensor.local_forecast_temperature`
- `sensor.local_forecast_pressurechange`
- `sensor.local_forecast_temperaturechange`

## Notes de compatibilité
- Les noms/attributs des capteurs restent proches du package YAML d'origine.
- L'intégration conserve la compatibilité des cartes tout en supprimant la dépendance aux templates/statistics YAML.
