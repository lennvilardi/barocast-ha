# Changelog

All notable changes to this project will be documented in this file.

## [0.3.0] - 2026-02-23
### Changed
- Breaking: all sensor entity IDs were renamed to the `sensor.barocast_forecast*` namespace.
- Updated examples and documentation to use the new sensor IDs.

### Migration
- Update dashboard cards/automations that reference old `sensor.local_forecast*` entities.
- Existing entities are auto-migrated to new IDs when possible.
- Use the new entity IDs:
  - `sensor.barocast_forecast`
  - `sensor.barocast_forecast_zambretti_detail`
  - `sensor.barocast_forecast_neg_zam_detail`
  - `sensor.barocast_forecast_pressure`
  - `sensor.barocast_forecast_temperature`
  - `sensor.barocast_forecast_pressure_change`
  - `sensor.barocast_forecast_temperature_change`

## [0.2.0] - 2026-02-23
### Changed
- Breaking: integration domain renamed to `barocast_ha` (legacy domain removed).
- Integration folder renamed to `custom_components/barocast_ha`.
- Integration display name harmonized to **Barocast HA** across manifest, config flow and docs.

### Migration
- Remove the existing legacy integration entry in Home Assistant.
- Install/update this release and add the integration again as **Barocast HA**.
- Sensor entity IDs are now `sensor.barocast_forecast*`.

## [0.1.0] - 2026-02-20
### Added
- First HACS custom integration version under `custom_components/local_weather_forecast`.
- Home Assistant config flow (language, pressure/temperature/wind entities, altitude, hemisphere, update interval).
- Forecast engine implementation for Zambretti + Negretti/Zambra.
- Sensors compatible with legacy card attributes.
- CI workflows for HACS validation, hassfest and secret scanning.
- Bilingual documentation (EN/FR).

### Fixed
- Language exception mapping bug in legacy YAML (`t_lang_exceptional`).
- Incorrect wind correction coefficients in Negretti/Zambra logic.
- Inconsistent pressure trend threshold in legacy YAML.
- Unreachable forecast mapping branch for Zambretti class `C`.
- Seasonal correction now honors configured hemisphere for both Zambretti and Negretti/Zambra paths.
- Temperature forecast now uses a weighted slope estimate and slope clamp to reduce spikes/noise.
- Pressure sea-level correction now uses a standard atmosphere fallback temperature when no temperature sensor is configured.
- Removed obsolete legacy YAML package/card files from the repository root.

---

# Journal des changements

Toutes les modifications notables de ce projet sont documentées dans ce fichier.

## [0.3.0] - 2026-02-23
### Modifications
- Changement majeur : tous les IDs d’entités capteurs sont renommés vers l’espace `sensor.barocast_forecast*`.
- Exemples et documentation mis à jour avec les nouveaux IDs.

### Migration
- Mettre à jour les cartes/automatisations qui référencent les anciennes entités `sensor.local_forecast*`.
- Les entités existantes sont migrées automatiquement vers les nouveaux IDs lorsque possible.
- Utiliser les nouveaux IDs :
  - `sensor.barocast_forecast`
  - `sensor.barocast_forecast_zambretti_detail`
  - `sensor.barocast_forecast_neg_zam_detail`
  - `sensor.barocast_forecast_pressure`
  - `sensor.barocast_forecast_temperature`
  - `sensor.barocast_forecast_pressure_change`
  - `sensor.barocast_forecast_temperature_change`

## [0.2.0] - 2026-02-23
### Modifications
- Changement majeur : domain d’intégration renommé vers `barocast_ha` (ancien domain supprimé).
- Dossier d’intégration renommé en `custom_components/barocast_ha`.
- Nom d’affichage harmonisé en **Barocast HA** dans le manifest, le config flow et la documentation.

### Migration
- Supprimer l’entrée d’intégration legacy existante dans Home Assistant.
- Installer/mettre à jour cette version puis ajouter à nouveau l’intégration sous **Barocast HA**.
- Les IDs d’entités capteurs sont désormais `sensor.barocast_forecast*`.

## [0.1.0] - 2026-02-20
### Ajouts
- Première version de l’intégration custom HACS dans `custom_components/local_weather_forecast`.
- Config flow Home Assistant (langue, entités pression/température/vent, altitude, hémisphère, intervalle).
- Implémentation du moteur de prévision Zambretti + Negretti/Zambra.
- Capteurs compatibles avec les attributs des cartes legacy.
- Workflows CI pour validation HACS, hassfest et scan de secrets.
- Documentation bilingue (EN/FR).

### Corrections
- Correction du mapping de langue exceptionnel dans le YAML legacy (`t_lang_exceptional`).
- Correction des coefficients de correction vent dans la logique Negretti/Zambra.
- Harmonisation du seuil de tendance de pression dans le YAML legacy.
- Correction d’une branche de mapping inatteignable pour la classe Zambretti `C`.
- La correction saisonnière respecte désormais l’hémisphère configuré pour les chemins Zambretti et Negretti/Zambra.
- La prévision température utilise désormais une estimation de pente pondérée avec plafonnement pour réduire pics/bruit.
- La correction de pression au niveau de la mer utilise une température standard de repli quand aucun capteur de température n’est configuré.
- Suppression des fichiers package/cartes YAML legacy obsolètes à la racine du dépôt.
