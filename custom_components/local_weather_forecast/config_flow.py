"""Config flow for Local Weather Forecast integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector

from .const import (
    CONF_ALTITUDE,
    CONF_HEMISPHERE,
    CONF_LANGUAGE,
    CONF_PRESSURE_ENTITY,
    CONF_PRESSURE_IS_SEA_LEVEL,
    CONF_TEMPERATURE_ENTITY,
    CONF_UPDATE_INTERVAL,
    CONF_WIND_DIRECTION_ENTITY,
    CONF_WIND_SPEED_ENTITY,
    DEFAULT_ALTITUDE,
    DEFAULT_HEMISPHERE,
    DEFAULT_LANGUAGE,
    DEFAULT_PRESSURE_IS_SEA_LEVEL,
    DEFAULT_UPDATE_INTERVAL_SECONDS,
    DOMAIN,
    HEMISPHERE_NORTH,
    HEMISPHERE_SOUTH,
    LANG_DE,
    LANG_EL,
    LANG_EN,
    LANG_FR,
    LANG_IT,
)

LANGUAGE_OPTIONS = [
    {"value": LANG_DE, "label": "Deutsch"},
    {"value": LANG_EN, "label": "English"},
    {"value": LANG_EL, "label": "Ελληνικά"},
    {"value": LANG_IT, "label": "Italiano"},
    {"value": LANG_FR, "label": "Français"},
]

HEMISPHERE_OPTIONS = [
    {"value": HEMISPHERE_NORTH, "label": "Northern hemisphere"},
    {"value": HEMISPHERE_SOUTH, "label": "Southern hemisphere"},
]


class LocalWeatherForecastConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Local Weather Forecast."""

    VERSION = 1

    @staticmethod
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> config_entries.OptionsFlow:
        """Return the options flow handler."""
        return LocalWeatherForecastOptionsFlow(config_entry)

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> config_entries.ConfigFlowResult:
        """Handle first step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        errors: dict[str, str] = {}
        if user_input is not None:
            clean_input = _clean_input(user_input)
            errors = self._validate_input(clean_input)

            if not errors:
                await self.async_set_unique_id(f"{DOMAIN}_{clean_input[CONF_PRESSURE_ENTITY]}")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title="Local Weather Forecast", data=clean_input)

        return self.async_show_form(
            step_id="user",
            data_schema=_build_schema(user_input),
            errors=errors,
        )

    def _validate_input(self, user_input: dict[str, Any]) -> dict[str, str]:
        """Validate form values."""
        errors: dict[str, str] = {}

        pressure_entity = user_input.get(CONF_PRESSURE_ENTITY)
        if pressure_entity is None or not self._entity_exists(pressure_entity):
            errors[CONF_PRESSURE_ENTITY] = "entity_not_found"
        elif not self._entity_is_numeric(pressure_entity):
            errors[CONF_PRESSURE_ENTITY] = "invalid_pressure"

        for optional_sensor in (
            CONF_TEMPERATURE_ENTITY,
            CONF_WIND_SPEED_ENTITY,
            CONF_WIND_DIRECTION_ENTITY,
        ):
            entity_id = user_input.get(optional_sensor)
            if entity_id and not self._entity_exists(entity_id):
                errors[optional_sensor] = "entity_not_found"

        return errors

    def _entity_exists(self, entity_id: str) -> bool:
        """Check if entity exists."""
        return self.hass.states.get(entity_id) is not None

    def _entity_is_numeric(self, entity_id: str) -> bool:
        """Check if entity state can be parsed as a float."""
        state = self.hass.states.get(entity_id)
        if state is None:
            return False
        try:
            float(state.state)
        except (TypeError, ValueError):
            return False
        return True


class LocalWeatherForecastOptionsFlow(config_entries.OptionsFlow):
    """Handle Local Weather Forecast options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self._config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> config_entries.ConfigFlowResult:
        """Manage options."""
        defaults = {**self._config_entry.data, **self._config_entry.options}

        if user_input is not None:
            clean_input = _clean_input(user_input)
            errors = _validate_with_hass(self.hass, clean_input)
            if not errors:
                return self.async_create_entry(title="", data=clean_input)
        else:
            errors = {}

        return self.async_show_form(
            step_id="init",
            data_schema=_build_schema(defaults),
            errors=errors,
        )


def _build_schema(defaults: dict[str, Any] | None) -> vol.Schema:
    """Build configuration schema for setup and options."""
    defaults = defaults or {}

    pressure_field = (
        vol.Required(CONF_PRESSURE_ENTITY, default=defaults[CONF_PRESSURE_ENTITY])
        if CONF_PRESSURE_ENTITY in defaults and defaults[CONF_PRESSURE_ENTITY]
        else vol.Required(CONF_PRESSURE_ENTITY)
    )

    temp_field = (
        vol.Optional(CONF_TEMPERATURE_ENTITY, default=defaults[CONF_TEMPERATURE_ENTITY])
        if CONF_TEMPERATURE_ENTITY in defaults and defaults[CONF_TEMPERATURE_ENTITY]
        else vol.Optional(CONF_TEMPERATURE_ENTITY)
    )
    wind_speed_field = (
        vol.Optional(CONF_WIND_SPEED_ENTITY, default=defaults[CONF_WIND_SPEED_ENTITY])
        if CONF_WIND_SPEED_ENTITY in defaults and defaults[CONF_WIND_SPEED_ENTITY]
        else vol.Optional(CONF_WIND_SPEED_ENTITY)
    )
    wind_direction_field = (
        vol.Optional(CONF_WIND_DIRECTION_ENTITY, default=defaults[CONF_WIND_DIRECTION_ENTITY])
        if CONF_WIND_DIRECTION_ENTITY in defaults and defaults[CONF_WIND_DIRECTION_ENTITY]
        else vol.Optional(CONF_WIND_DIRECTION_ENTITY)
    )
    schema: dict[Any, Any] = {
        pressure_field: selector.EntitySelector(selector.EntitySelectorConfig(domain="sensor")),
        vol.Required(
            CONF_LANGUAGE,
            default=defaults.get(CONF_LANGUAGE, DEFAULT_LANGUAGE),
        ): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=LANGUAGE_OPTIONS,
                mode=selector.SelectSelectorMode.DROPDOWN,
            )
        ),
        vol.Required(
            CONF_PRESSURE_IS_SEA_LEVEL,
            default=defaults.get(CONF_PRESSURE_IS_SEA_LEVEL, DEFAULT_PRESSURE_IS_SEA_LEVEL),
        ): selector.BooleanSelector(),
        vol.Required(
            CONF_ALTITUDE,
            default=defaults.get(CONF_ALTITUDE, DEFAULT_ALTITUDE),
        ): selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=-500,
                max=9000,
                step=1,
                mode=selector.NumberSelectorMode.BOX,
                unit_of_measurement="m",
            )
        ),
        vol.Required(
            CONF_HEMISPHERE,
            default=defaults.get(CONF_HEMISPHERE, DEFAULT_HEMISPHERE),
        ): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=HEMISPHERE_OPTIONS,
                mode=selector.SelectSelectorMode.DROPDOWN,
            )
        ),
        vol.Required(
            CONF_UPDATE_INTERVAL,
            default=defaults.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL_SECONDS),
        ): selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=30,
                max=3600,
                step=10,
                mode=selector.NumberSelectorMode.BOX,
                unit_of_measurement="s",
            )
        ),
        temp_field: selector.EntitySelector(selector.EntitySelectorConfig(domain="sensor")),
        wind_speed_field: selector.EntitySelector(selector.EntitySelectorConfig(domain="sensor")),
        wind_direction_field: selector.EntitySelector(selector.EntitySelectorConfig(domain="sensor")),
    }

    return vol.Schema(schema)


def _clean_input(user_input: dict[str, Any]) -> dict[str, Any]:
    """Normalize and clean form input."""
    clean = dict(user_input)

    # Optional entity selectors can submit empty strings; drop them so
    # runtime code can treat the sensor as "not configured".
    for key in (
        CONF_TEMPERATURE_ENTITY,
        CONF_WIND_SPEED_ENTITY,
        CONF_WIND_DIRECTION_ENTITY,
    ):
        value = clean.get(key)
        if not value:
            clean.pop(key, None)

    clean[CONF_ALTITUDE] = float(clean.get(CONF_ALTITUDE, DEFAULT_ALTITUDE))
    clean[CONF_UPDATE_INTERVAL] = int(clean.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL_SECONDS))
    return clean


def _validate_with_hass(hass, user_input: dict[str, Any]) -> dict[str, str]:
    """Validate form values with access to hass."""
    errors: dict[str, str] = {}

    pressure_entity = user_input.get(CONF_PRESSURE_ENTITY)
    pressure_state = hass.states.get(pressure_entity) if pressure_entity else None
    if pressure_state is None:
        errors[CONF_PRESSURE_ENTITY] = "entity_not_found"
    else:
        try:
            float(pressure_state.state)
        except (TypeError, ValueError):
            errors[CONF_PRESSURE_ENTITY] = "invalid_pressure"

    for optional_sensor in (
        CONF_TEMPERATURE_ENTITY,
        CONF_WIND_SPEED_ENTITY,
        CONF_WIND_DIRECTION_ENTITY,
    ):
        entity_id = user_input.get(optional_sensor)
        if entity_id and hass.states.get(entity_id) is None:
            errors[optional_sensor] = "entity_not_found"

    return errors
