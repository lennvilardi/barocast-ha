## Release {{VERSION}}

### Highlights
- Stable HACS integration release for Barocast HA.
- Config flow setup in Home Assistant.
- Forecast engine improvements and bug fixes.

### What changed
- Added/updated sensors for forecast, details, pressure and temperature changes.
- Improved algorithm consistency (trend threshold, wind correction, mapping fixes).
- Added CI checks (HACS, hassfest, gitleaks).

### Upgrade notes
- Restart Home Assistant after update.
- Breaking: domain renamed from `local_weather_forecast` to `barocast_ha`.
- Review integration options if you changed sensor entity IDs.

### Links
- Integration docs: `custom_components/barocast_ha/README.md`
- Full changelog: `CHANGELOG.md`
