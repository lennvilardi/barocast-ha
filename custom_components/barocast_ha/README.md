# Barocast HA (HACS Integration)

A Home Assistant custom integration that computes a 12-hour local forecast from local sensors.

## Domain
- Current domain: `barocast_ha`
- Legacy domain removed in `v0.2.0` (breaking rename)

## What it does
- Implements Zambretti + Negretti/Zambra pressure-based forecast models.
- Provides forecast text, trend, rain probability proxies and icon hints.
- Exposes sensors compatible with legacy YAML cards.
- Adds a full Home Assistant config UI (config flow + options flow).
- Uses a weighted short-term temperature trend estimator (less noise than single-point extrapolation).

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
- `sensor.barocast_forecast`
- `sensor.barocast_forecast_zambretti_detail`
- `sensor.barocast_forecast_neg_zam_detail`
- `sensor.barocast_forecast_pressure`
- `sensor.barocast_forecast_temperature`
- `sensor.barocast_forecast_pressure_change`
- `sensor.barocast_forecast_temperature_change`

Main sensor extra attributes also include:
- `temperature_trend_slope_1h`

## Compatibility notes
- Sensor names/attributes are intentionally close to the original YAML package.
- The integration keeps card compatibility while replacing template/statistics dependencies.
- Sensor entity names are `sensor.barocast_forecast*`.

---

# Version Française

Intégration custom Home Assistant qui calcule une prévision locale 12h à partir de capteurs locaux.

## Domain
- Domain actuel : `barocast_ha`
- Ancien domain retiré en `v0.2.0` (renommage majeur)

## Ce que fait l'intégration
- Implémente les modèles de prévision basés sur la pression : Zambretti + Negretti/Zambra.
- Fournit texte de prévision, tendance, proxy de probabilité de pluie et icônes.
- Expose des capteurs compatibles avec les anciennes cartes YAML.
- Ajoute une configuration complète via l'interface Home Assistant (config flow + options flow).
- Utilise une estimation pondérée de tendance température à court terme (moins de bruit qu’une extrapolation sur un seul point).

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
- `sensor.barocast_forecast`
- `sensor.barocast_forecast_zambretti_detail`
- `sensor.barocast_forecast_neg_zam_detail`
- `sensor.barocast_forecast_pressure`
- `sensor.barocast_forecast_temperature`
- `sensor.barocast_forecast_pressure_change`
- `sensor.barocast_forecast_temperature_change`

Les attributs du capteur principal incluent aussi :
- `temperature_trend_slope_1h`

## Notes de compatibilité
- Les noms/attributs des capteurs restent proches du package YAML d'origine.
- L'intégration conserve la compatibilité des cartes tout en supprimant la dépendance aux templates/statistics YAML.
- Les noms d’entités capteurs sont `sensor.barocast_forecast*`.
