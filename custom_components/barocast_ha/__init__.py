"""The Barocast HA integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .const import DOMAIN
from .coordinator import BarocastHACoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]
LOGGER = logging.getLogger(__name__)

ENTITY_ID_BY_KEY: dict[str, str] = {
    "main": "sensor.barocast_forecast",
    "zambretti_detail": "sensor.barocast_forecast_zambretti_detail",
    "neg_zam_detail": "sensor.barocast_forecast_neg_zam_detail",
    "pressure": "sensor.barocast_forecast_pressure",
    "temperature": "sensor.barocast_forecast_temperature",
    "pressure_change": "sensor.barocast_forecast_pressure_change",
    "temperature_change": "sensor.barocast_forecast_temperature_change",
}


BarocastHAConfigEntry = ConfigEntry[BarocastHACoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: BarocastHAConfigEntry) -> bool:
    """Set up Barocast HA from a config entry."""
    _async_migrate_sensor_entity_ids(hass, entry)

    coordinator = BarocastHACoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: BarocastHAConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(hass: HomeAssistant, entry: BarocastHAConfigEntry) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)


def _async_migrate_sensor_entity_ids(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Rename legacy sensor entity IDs to the Barocast namespace."""
    entity_registry = er.async_get(hass)
    entries = er.async_entries_for_config_entry(entity_registry, entry.entry_id)

    for entity in entries:
        if entity.domain != "sensor":
            continue

        for key, new_entity_id in ENTITY_ID_BY_KEY.items():
            if not entity.unique_id.endswith(f"_{key}"):
                continue
            if entity.entity_id == new_entity_id:
                break
            try:
                entity_registry.async_update_entity(entity.entity_id, new_entity_id=new_entity_id)
                LOGGER.info("Renamed %s -> %s", entity.entity_id, new_entity_id)
            except ValueError as err:
                LOGGER.warning(
                    "Could not rename %s to %s: %s",
                    entity.entity_id,
                    new_entity_id,
                    err,
                )
            break
