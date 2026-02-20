"""Coordinator for Local Weather Forecast integration."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

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
    DEFAULT_UPDATE_INTERVAL,
    HEMISPHERE_NORTH,
    TITLE_BY_LANG,
)
from .forecast_engine import (
    get_language_index,
    neg_zam_detail,
    neg_zam_forecast,
    pressure_to_sea_level,
    pressure_trend_output,
    short_temperature_forecast,
    short_term_conditions,
    wind_compass_text,
    wind_factor,
    wind_speed_factor,
    zambretti_detail,
    zambretti_forecast,
)

LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class LocalWeatherForecastData:
    """Runtime forecast snapshot used by entities."""

    main_state: str
    main_attributes: dict[str, Any]
    zambretti_state: str
    zambretti_attributes: dict[str, Any]
    neg_zam_state: str
    neg_zam_attributes: dict[str, Any]
    pressure: float
    temperature: float
    pressure_change: float
    temperature_change: float


class LocalWeatherForecastCoordinator(DataUpdateCoordinator[LocalWeatherForecastData]):
    """Handle periodic forecast updates."""

    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize coordinator."""
        self.config_entry = entry
        # We keep local rolling histories to emulate HA statistics sensors
        # (3h pressure delta / 1h temperature delta) without extra entities.
        self._pressure_history: deque[tuple[datetime, float]] = deque()
        self._temperature_history: deque[tuple[datetime, float]] = deque()
        super().__init__(
            hass,
            logger=LOGGER,
            name="Local Weather Forecast",
            update_interval=self._update_interval,
        )

    @property
    def _update_interval(self) -> timedelta:
        """Return update interval from config."""
        interval_seconds = int(self._cfg(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL.total_seconds()))
        interval_seconds = min(max(interval_seconds, 30), 3600)
        return timedelta(seconds=interval_seconds)

    def _cfg(self, key: str, default: Any = None) -> Any:
        """Get option value with fallback to data and then default."""
        if key in self.config_entry.options:
            return self.config_entry.options[key]
        return self.config_entry.data.get(key, default)

    def _state_as_float(self, entity_id: str, *, required: bool) -> float | None:
        """Read entity state as float."""
        state = self.hass.states.get(entity_id)
        if state is None:
            if required:
                raise UpdateFailed(f"Entity not found: {entity_id}")
            return None

        try:
            return float(state.state)
        except (TypeError, ValueError):
            if required:
                raise UpdateFailed(f"Entity state is not numeric: {entity_id}")
            return None

    @staticmethod
    def _append_and_prune(
        history: deque[tuple[datetime, float]],
        now: datetime,
        value: float,
        max_age: timedelta,
    ) -> None:
        """Add point and prune old values."""
        history.append((now, value))
        cutoff = now - max_age
        while history and history[0][0] < cutoff:
            history.popleft()

    @staticmethod
    def _change_from_history(history: deque[tuple[datetime, float]], current: float) -> float:
        """Compute change between current value and oldest sample in window."""
        if not history:
            return 0.0
        return current - history[0][1]

    async def _async_update_data(self) -> LocalWeatherForecastData:
        """Fetch and calculate forecast data."""
        pressure_entity = self._cfg(CONF_PRESSURE_ENTITY)
        if not pressure_entity:
            raise UpdateFailed("Pressure entity is not configured")

        language = self._cfg(CONF_LANGUAGE, DEFAULT_LANGUAGE)
        language_index = get_language_index(language)

        pressure_raw = self._state_as_float(pressure_entity, required=True)
        assert pressure_raw is not None

        temp_entity = self._cfg(CONF_TEMPERATURE_ENTITY)
        wind_speed_entity = self._cfg(CONF_WIND_SPEED_ENTITY)
        wind_direction_entity = self._cfg(CONF_WIND_DIRECTION_ENTITY)

        temperature = self._state_as_float(temp_entity, required=False) if temp_entity else None
        wind_speed = self._state_as_float(wind_speed_entity, required=False) if wind_speed_entity else None
        wind_direction = (
            self._state_as_float(wind_direction_entity, required=False) if wind_direction_entity else None
        )

        temperature = 0.0 if temperature is None else temperature
        wind_speed = 0.0 if wind_speed is None else wind_speed
        wind_direction = 0.0 if wind_direction is None else wind_direction

        pressure_is_sea_level = bool(self._cfg(CONF_PRESSURE_IS_SEA_LEVEL, DEFAULT_PRESSURE_IS_SEA_LEVEL))
        altitude = float(self._cfg(CONF_ALTITUDE, DEFAULT_ALTITUDE))

        # If pressure is not sea-level corrected, normalize it with altitude.
        p0 = (
            pressure_raw
            if pressure_is_sea_level
            else pressure_to_sea_level(pressure_raw, temperature, altitude)
        )

        now = dt_util.now()

        self._append_and_prune(self._pressure_history, now, p0, timedelta(hours=3))
        self._append_and_prune(self._temperature_history, now, temperature, timedelta(hours=1))

        pressure_change = self._change_from_history(self._pressure_history, p0)
        temperature_change = self._change_from_history(self._temperature_history, temperature)

        wind_speed_flag = wind_speed_factor(wind_speed)
        wind_direction_factor = wind_factor(wind_direction)
        wind_direction_text = wind_compass_text(wind_direction)
        hemisphere = self._cfg(CONF_HEMISPHERE, DEFAULT_HEMISPHERE)
        is_northern_hemisphere = hemisphere == HEMISPHERE_NORTH

        short_condition, pressure_system = short_term_conditions(p0, language_index)
        zambretti_text, zambretti_type, zambretti_letter = zambretti_forecast(
            p0,
            pressure_change,
            wind_direction,
            wind_speed,
            is_northern_hemisphere,
            language_index,
            now,
        )

        neg_zam_text, neg_zam_number, neg_zam_letter = neg_zam_forecast(
            p0,
            pressure_change,
            wind_direction,
            wind_speed,
            is_northern_hemisphere,
            language_index,
            now,
        )

        sun_state = self.hass.states.get("sun.sun")
        is_night = bool(sun_state and sun_state.state == "below_horizon")

        zambretti_detail_payload = zambretti_detail(zambretti_type, is_night, now)
        neg_zam_detail_payload = neg_zam_detail(neg_zam_number, is_night, now)

        forecast_temp_value, forecast_temp_interval = short_temperature_forecast(
            temperature,
            temperature_change,
            float(zambretti_detail_payload["first_time"][1]),
            float(zambretti_detail_payload["second_time"][1]),
        )

        trend_text, trend_code = pressure_trend_output(pressure_change, language_index)

        main_attributes = {
            "language": language_index,
            "temperature": round(temperature, 1),
            "p0": round(p0, 1),
            "wind_direction": [
                wind_direction_factor,
                round(wind_direction, 1),
                wind_direction_text,
                wind_speed_flag,
            ],
            "forecast_short_term": [short_condition, pressure_system],
            "forecast_zambretti": [zambretti_text, zambretti_type, zambretti_letter],
            "forecast_neg_zam": [neg_zam_text, neg_zam_number, neg_zam_letter],
            "forecast_pressure_trend": [trend_text, trend_code],
            "forecast_temp_short": [forecast_temp_value, forecast_temp_interval],
            "pressure_change_3h": round(pressure_change, 2),
            "temperature_change_1h": round(temperature_change, 2),
        }

        return LocalWeatherForecastData(
            main_state=TITLE_BY_LANG.get(language, TITLE_BY_LANG[DEFAULT_LANGUAGE]),
            main_attributes=main_attributes,
            zambretti_state=f"More details on zambretti forecast ({zambretti_type + 1})",
            zambretti_attributes=zambretti_detail_payload,
            neg_zam_state=f"More details on neg_zam forecast ({neg_zam_number + 1})",
            neg_zam_attributes=neg_zam_detail_payload,
            pressure=round(p0, 1),
            temperature=round(temperature, 1),
            pressure_change=round(pressure_change, 2),
            temperature_change=round(temperature_change, 2),
        )
