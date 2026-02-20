"""Constants for Local Weather Forecast integration."""

from __future__ import annotations

from datetime import timedelta

DOMAIN = "local_weather_forecast"

CONF_LANGUAGE = "language"
CONF_PRESSURE_ENTITY = "pressure_entity"
CONF_TEMPERATURE_ENTITY = "temperature_entity"
CONF_WIND_SPEED_ENTITY = "wind_speed_entity"
CONF_WIND_DIRECTION_ENTITY = "wind_direction_entity"
CONF_PRESSURE_IS_SEA_LEVEL = "pressure_is_sea_level"
CONF_ALTITUDE = "altitude"
CONF_HEMISPHERE = "hemisphere"
CONF_UPDATE_INTERVAL = "update_interval"

HEMISPHERE_NORTH = "north"
HEMISPHERE_SOUTH = "south"

LANG_DE = "de"
LANG_EN = "en"
LANG_EL = "el"
LANG_IT = "it"
LANG_FR = "fr"
LANGUAGE_CODES = [LANG_DE, LANG_EN, LANG_EL, LANG_IT, LANG_FR]
LANGUAGE_INDEX = {code: index for index, code in enumerate(LANGUAGE_CODES)}

DEFAULT_LANGUAGE = LANG_EN
DEFAULT_PRESSURE_IS_SEA_LEVEL = True
DEFAULT_ALTITUDE = 0.0
DEFAULT_HEMISPHERE = HEMISPHERE_NORTH
DEFAULT_UPDATE_INTERVAL_SECONDS = 300
DEFAULT_UPDATE_INTERVAL = timedelta(seconds=DEFAULT_UPDATE_INTERVAL_SECONDS)

PRESSURE_TREND_THRESHOLD = 1.6
WIND_CALM_THRESHOLD_KMH = 1.0
TEMPERATURE_STANDARD_ATMOSPHERE_C = 15.0
TEMPERATURE_MAX_FORECAST_SLOPE_C_PER_H = 4.0

TITLE_BY_LANG = {
    LANG_DE: "Lokale Wettervorhersage",
    LANG_EN: "12hr Local Weather Forecast",
    LANG_EL: "Τοπική πρόγνωση καιρού",
    LANG_IT: "Previsioni meteorologiche locali",
    LANG_FR: "Prévisions météorologiques locales",
}
