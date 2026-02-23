# Changelog

All notable changes to this project will be documented in this file.

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
