## Release {{VERSION}}

### Points clés
- Version stable de l’intégration HACS Barocast HA.
- Configuration via l’interface Home Assistant (config flow).
- Améliorations du moteur de prévision et corrections de bugs.

### Changements
- Ajout/mise à jour des capteurs de prévision, détails, variations pression/température.
- Cohérence algorithmique améliorée (seuil de tendance, correction vent, mapping).
- Ajout des contrôles CI (HACS, hassfest, gitleaks).

### Notes de mise à jour
- Redémarrer Home Assistant après mise à jour.
- Changement majeur : domain renommé de `local_weather_forecast` vers `barocast_ha`.
- Vérifier les options de l’intégration si les entités capteurs ont changé.

### Liens
- Documentation intégration : `custom_components/barocast_ha/README.md`
- Changelog complet : `CHANGELOG.md`
