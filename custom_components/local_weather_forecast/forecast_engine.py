"""Forecast calculation engine for Local Weather Forecast."""

from __future__ import annotations

from datetime import datetime, timedelta
from math import floor

from .const import (
    DEFAULT_LANGUAGE,
    LANGUAGE_INDEX,
    PRESSURE_TREND_THRESHOLD,
    WIND_CALM_THRESHOLD_KMH,
)

SHORT_CONDITIONS: tuple[tuple[str, ...], ...] = (
    ("stürmisch", "Stormy", "θυελλώδης", "Tempestoso", "Orageux"),
    ("regnerisch", "Rainy", "Βροχερός", "Piovoso", "Pluvieux"),
    ("wechselhaft", "Mixed", "Μεταβλητός", "Variabile", "Variable"),
    ("sonnig", "Sunny", "Ηλιόλουστος", "Soleggiato", "Ensoleillé"),
    ("sehr trocken", "Extra Dry", "Πολύ ξηρός", "Molto Secco", "Très Sec"),
)

PRESSURE_SYSTEMS: tuple[tuple[str, ...], ...] = (
    (
        "Tiefdruckgebiet",
        "Low Pressure System",
        "σύστημα χαμηλής πίεσης",
        "Bassa Pressione",
        "Système de basse pression",
    ),
    ("Normal", "Normal", "φυσιολογικός", "Normale", "Normal"),
    (
        "Hochdruckgebiet",
        "High Pressure System",
        "σύστημα υψηλής πίεσης",
        "Zona Alta Pressione",
        "Système de haute pression",
    ),
)

FORECAST_TEXTS: tuple[tuple[str, ...], ...] = (
    (
        "Beständiges Schönwetter!",
        "Settled Fine",
        "Σταθερός καλός καιρός!",
        "Bel tempo stabile!",
        "Beau temps stable!",
    ),
    ("Schönes Wetter!", "Fine", "Ωραίος καιρός!", "Bel tempo!", "Beau temps!"),
    (
        "Es wird schöner.",
        "Becoming Fine",
        "Θα καλυτερεύσει.",
        "Miglioramento in corso.",
        "Le temps s'améliore.",
    ),
    (
        "Schön, wird wechselhaft.",
        "Fine, Becoming Less Settled",
        "Μεταβλητός.",
        "Bello, ma diventa instabile.",
        "Beau, devient instable.",
    ),
    (
        "Schön, Regenschauer möglich.",
        "Fine, Possibly Showers",
        "Πιθανή βροχή.",
        "Bello, possibili rovesci.",
        "Beau, averses possibles.",
    ),
    (
        "Heiter bis wolkig, Besserung zu erwarten.",
        "Fairly Fine, Improving",
        "Αίθριος έως νεφελώδης, αναμένεται βελτίωση.",
        "Sereno con nuvole, miglioramento atteso.",
        "Éclaircies avec nuages, amélioration attendue.",
    ),
    (
        "Heiter bis wolkig, anfangs evtl. Schauer.",
        "Fairly Fine, Possibly Showers, Early",
        "Αίθριος έως συννεφιασμένος, πιθανώς βροχές στην αρχή.",
        "Sereno con nuvole, possibili rovesci all'inizio.",
        "Éclaircies avec nuages, averses possibles au début.",
    ),
    (
        "Heiter bis wolkig, später Regen.",
        "Fairly Fine, Showery Later",
        "Αίθριος έως συννεφιασμένος, αργότερα βροχή.",
        "Sereno con nuvole, pioggia in arrivo.",
        "Éclaircies avec nuages, pluie plus tard.",
    ),
    (
        "Anfangs noch Schauer, dann Besserung.",
        "Showery Early, Improving",
        "Βροχόπτωση στην αρχή και μετά βελτίωση.",
        "Rovesci iniziali, poi miglioramento.",
        "Averses au début, puis amélioration.",
    ),
    (
        "Wechselhaft mit Schauern",
        "Changeable, Mending",
        "Εναλλαγή με βροχόπτωση.",
        "Variabile con rovesci.",
        "Variable avec averses.",
    ),
    (
        "Heiter bis wolkig, vereinzelt Regen.",
        "Fairly Fine, Showers Likely",
        "Αίθριος έως συννεφιασμένος, κατά διαστήματα βροχή.",
        "Sereno con nuvole, pioggia probabile.",
        "Éclaircies avec nuages, averses probables.",
    ),
    (
        "Unbeständig, später Aufklarung.",
        "Rather Unsettled, Clearing Later",
        "Ασταθής, αργότερα καθάρος.",
        "Instabile, schiarite più tardi.",
        "Instable, éclaircies plus tard.",
    ),
    (
        "Unbeständig, evtl. Besserung.",
        "Unsettled, Probably Improving",
        "Ασταθής, πιθανώς βελτίωση.",
        "Instabile, probabile miglioramento.",
        "Instable, amélioration possible.",
    ),
    (
        "Regnerisch mit heiteren Phasen.",
        "Showery, Bright Intervals",
        "Καθαρός με διαστήματα βροχής.",
        "Rovesci con schiarite.",
        "Pluvieux avec éclaircies.",
    ),
    (
        "Regnerisch, wird unbeständiger.",
        "Showery, Becoming More Unsettled",
        "Βροχερό, όλο και πιο ασταθές.",
        "Rovesci, sempre più instabile.",
        "Pluvieux, devient plus instable.",
    ),
    (
        "Wechselhaft mit etwas Regen.",
        "Changeable, Some Rain",
        "Αλλάζει με λίγη βροχή.",
        "Variabile con qualche pioggia.",
        "Variable avec un peu de pluie.",
    ),
    (
        "Unbeständig mit heiteren Phasen.",
        "Unsettled, Short Fine Intervals",
        "Άστατα, μικρά καθαρά διαστήματα",
        "Instabile con brevi schiarite.",
        "Instable avec courtes éclaircies.",
    ),
    (
        "Unbeständig, später Regen.",
        "Unsettled, Rain Later",
        "Άστατη, αργότερα βροχή.",
        "Instabile, pioggia più tardi.",
        "Instable, pluie plus tard.",
    ),
    (
        "Unbeständig mit etwas Regen.",
        "Unsettled, Rain At Times",
        "Άστατος με λίγη βροχή.",
        "Instabile con qualche pioggia.",
        "Instable avec quelques pluies.",
    ),
    (
        "Wechselhaft und regnerisch",
        "Very Unsettled, Finer At Times",
        "Μεταβλητός και βροχερός.",
        "Variabile e piovoso.",
        "Variable et pluvieux.",
    ),
    (
        "Gelegentlich Regen, Verschlechterung.",
        "Rain At Times, Worse Later",
        "Περιστασιακές βροχές, επιδείνωση.",
        "Pioggia occasionale, peggiora più tardi.",
        "Pluie occasionnelle, dégradation ensuite.",
    ),
    (
        "Zuweilen Regen, sehr unbeständig.",
        "Rain At Times, Becoming Very Unsettled",
        "Βροχή κατά περιόδους, πολύ ασταθής.",
        "Pioggia a tratti, molto instabile.",
        "Pluie par moments, devient très instable.",
    ),
    (
        "Häufiger Regen.",
        "Rain At Frequent Intervals",
        "Συχνή βροχή.",
        "Pioggia frequente.",
        "Pluie fréquente.",
    ),
    (
        "Regen, sehr unbeständig.",
        "Very Unsettled, Rain",
        "Βροχή, πολύ ασταθής.",
        "Molto instabile, pioggia.",
        "Très instable, pluie.",
    ),
    (
        "Stürmisch, evtl. Besserung.",
        "Stormy, Possibly Improving",
        "Θυελλώδης, πιθανώς βελτίωση.",
        "Tempestoso, possibile miglioramento.",
        "Orageux, amélioration possible.",
    ),
    (
        "Stürmisch mit viel Regen.",
        "Stormy, Much Rain",
        "Καταιγίδα με πολλές βροχές.",
        "Tempestoso con molta pioggia.",
        "Orageux avec beaucoup de pluie.",
    ),
)

EXCEPTIONAL_TEXT = (
    "außergewöhnliches Wetter,",
    "Exceptional Weather,",
    "Εξαιρετικός καιρός,",
    "Tempo eccezionale,",
    "Temps exceptionnel,",
)

TREND_TEXTS = (
    ("fallend", "Falling", "πέφτοντας", "in calo", "en baisse"),
    ("steigend", "Rising", "αυξανόμενη", "in aumento", "en hausse"),
    ("stabil", "Steady", "σταθερή", "stabile", "stable"),
)

# Map "severity type" (0..25 used by the legacy card) to classical
# Zambretti numbers. This preserves compatibility with the original YAML.
TYPE_TO_Z: dict[int, tuple[int, ...]] = {
    0: (1, 10, 20),
    1: (2, 11, 21),
    2: (22,),
    3: (3,),
    4: (12,),
    5: (23,),
    6: (24,),
    7: (4,),
    8: (25,),
    9: (26,),
    10: (13,),
    11: (27,),
    12: (28,),
    13: (14,),
    14: (5,),
    15: (15,),
    16: (29,),
    17: (6,),
    18: (16,),
    19: (30,),
    20: (7,),
    21: (8,),
    22: (17,),
    23: (9, 18),
    24: (31,),
    25: (19, 32),
}

Z_TO_TYPE: dict[int, int] = {
    z: forecast_type for forecast_type, z_values in TYPE_TO_Z.items() for z in z_values
}

TYPE_LETTERS = tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

RISE_OPT = (25, 25, 25, 24, 24, 19, 16, 12, 11, 9, 8, 6, 5, 2, 1, 1, 0, 0, 0, 0, 0, 0)
STEADY_OPT = (
    25,
    25,
    25,
    25,
    25,
    25,
    23,
    23,
    22,
    18,
    15,
    13,
    10,
    4,
    1,
    1,
    0,
    0,
    0,
    0,
    0,
    0,
)
FALL_OPT = (25, 25, 25, 25, 25, 25, 25, 25, 23, 23, 21, 20, 17, 14, 7, 3, 1, 1, 1, 0, 0, 0)

ICON_CONDITIONS = (
    ("mdi:weather-sunny", "mdi:weather-night"),
    ("mdi:weather-partly-cloudy", "mdi:weather-night-partly-cloudy"),
    ("mdi:weather-partly-rainy", "mdi:weather-partly-rainy"),
    ("mdi:weather-cloudy", "mdi:weather-cloudy"),
    ("mdi:weather-rainy", "mdi:weather-rainy"),
    ("mdi:weather-pouring", "mdi:weather-pouring"),
    ("mdi:weather-lightning-rainy", "mdi:weather-lightning-rainy"),
)

ZAMBRETTI_FORECAST_BY_CODE = {
    1: (0, 0),
    2: (1, 1),
    3: (2, 1),
    4: (1, 2),
    5: (1, 1),
    6: (1, 0),
    7: (2, 1),
    8: (1, 4),
    9: (4, 2),
    10: (4, 4),
    11: (1, 1),
    12: (3, 1),
    13: (3, 3),
    14: (2, 2),
    15: (4, 5),
    16: (4, 4),
    17: (2, 2),
    18: (2, 4),
    19: (2, 2),
    20: (5, 5),
    21: (2, 4),
    22: (4, 4),
    23: (4, 4),
    24: (6, 4),
    25: (6, 6),
}

NEG_ZAM_FORECAST_BY_CODE = {
    1: (0, 0),
    2: (1, 1),
    3: (2, 1),
    4: (1, 2),
    5: (2, 2),
    6: (2, 1),
    7: (2, 1),
    8: (1, 4),
    9: (4, 2),
    10: (4, 4),
    11: (2, 2),
    12: (3, 1),
    13: (3, 3),
    14: (2, 2),
    15: (4, 5),
    16: (4, 4),
    17: (2, 2),
    18: (2, 4),
    19: (2, 2),
    20: (5, 5),
    21: (2, 4),
    22: (4, 4),
    23: (4, 4),
    24: (6, 4),
    25: (6, 6),
}


def get_language_index(language_code: str) -> int:
    """Return the language index from language code."""
    return LANGUAGE_INDEX.get(language_code, LANGUAGE_INDEX[DEFAULT_LANGUAGE])


def pressure_to_sea_level(pressure_hpa: float, temp_c: float, altitude_m: float) -> float:
    """Calculate sea-level pressure from local pressure."""
    return pressure_hpa * (1 - ((0.0065 * altitude_m) / (temp_c + (0.0065 * altitude_m) + 273.15))) ** (
        -5.257
    )


def pressure_trend_index(pressure_change_3h: float) -> int:
    """Return trend index: -1 falling, 0 steady, 1 rising."""
    if pressure_change_3h <= -PRESSURE_TREND_THRESHOLD:
        return -1
    if pressure_change_3h >= PRESSURE_TREND_THRESHOLD:
        return 1
    return 0


def pressure_trend_output(pressure_change_3h: float, language_index: int) -> tuple[str, str]:
    """Return text and trend code used by the legacy card."""
    trend = pressure_trend_index(pressure_change_3h)
    if trend < 0:
        return TREND_TEXTS[0][language_index], "0"
    if trend > 0:
        return TREND_TEXTS[1][language_index], "1"
    return TREND_TEXTS[2][language_index], "2"


def wind_speed_factor(wind_speed_kmh: float) -> int:
    """Return 0 when calm, 1 when there is wind."""
    return 0 if wind_speed_kmh < WIND_CALM_THRESHOLD_KMH else 1


def wind_factor(wind_direction_deg: float) -> int:
    """Return wind factor used by the original template implementation."""
    if 135 <= wind_direction_deg <= 225:
        return 2
    if wind_direction_deg >= 315 or wind_direction_deg <= 45:
        return 0
    return 1


def wind_compass_text(wind_direction_deg: float) -> str:
    """Convert degrees to a 16-point compass text."""
    direction = wind_direction_deg % 360
    if 11.25 < direction <= 33.75:
        return "N"
    if 33.75 < direction <= 56.25:
        return "NE"
    if 56.25 < direction <= 78.75:
        return "ENE"
    if 78.75 < direction <= 101.25:
        return "E"
    if 101.25 < direction <= 123.75:
        return "ESE"
    if 123.75 < direction <= 146.25:
        return "SE"
    if 146.25 < direction <= 168.75:
        return "SSE"
    if 168.75 < direction <= 191.25:
        return "S"
    if 191.25 < direction <= 213.75:
        return "SSW"
    if 213.75 < direction <= 236.25:
        return "SW"
    if 236.25 < direction <= 258.75:
        return "WSW"
    if 258.75 < direction <= 281.25:
        return "W"
    if 281.25 < direction <= 303.75:
        return "WNW"
    if 303.75 < direction <= 326.25:
        return "NW"
    if 326.25 < direction <= 348.75:
        return "NNW"
    return "N"


def short_term_conditions(p0_hpa: float, language_index: int) -> tuple[str, str]:
    """Return short-term conditions and pressure system text."""
    if p0_hpa < 980:
        return SHORT_CONDITIONS[0][language_index], PRESSURE_SYSTEMS[0][language_index]
    if p0_hpa < 1000:
        return SHORT_CONDITIONS[1][language_index], PRESSURE_SYSTEMS[0][language_index]
    if p0_hpa < 1020:
        return SHORT_CONDITIONS[2][language_index], PRESSURE_SYSTEMS[1][language_index]
    if p0_hpa < 1040:
        return SHORT_CONDITIONS[3][language_index], PRESSURE_SYSTEMS[2][language_index]
    return SHORT_CONDITIONS[4][language_index], PRESSURE_SYSTEMS[2][language_index]


def _forecast_type_from_z(z_value: int) -> int:
    """Map a Zambretti number to the forecast severity index."""
    return Z_TO_TYPE.get(z_value, 9)


def forecast_letter_from_number(z_number: int) -> str:
    """Return forecast letter code from raw Zambretti number."""
    if z_number == 0:
        return "none"
    forecast_type = _forecast_type_from_z(z_number)
    return TYPE_LETTERS[forecast_type]


def _is_summer(now: datetime, is_northern_hemisphere: bool) -> bool:
    """Return whether current month is in the algorithm summer range.

    The legacy rule uses months 3..10 for the northern hemisphere.
    For southern hemisphere we mirror that rule by inverting the season flag.
    """
    northern_summer = 2 < now.month < 11
    return northern_summer if is_northern_hemisphere else not northern_summer


def zambretti_forecast(
    p0_hpa: float,
    pressure_change_3h: float,
    wind_direction_deg: float,
    wind_speed_kmh: float,
    is_northern_hemisphere: bool,
    language_index: int,
    now: datetime,
) -> tuple[str, int, str]:
    """Calculate Zambretti forecast text, index and letter."""
    trend = pressure_trend_index(pressure_change_3h)
    is_summer = _is_summer(now, is_northern_hemisphere)

    if trend < 0:
        z_raw = int(round(127 - 0.12 * p0_hpa, 0))
    elif trend == 0:
        z_raw = int(round(144 - 0.13 * p0_hpa, 0))
        if not is_summer:
            z_raw -= 1
    else:
        z_raw = int(round(185 - 0.16 * p0_hpa, 0))
        if is_summer:
            z_raw += 1

    z_raw += wind_factor(wind_direction_deg) * wind_speed_factor(wind_speed_kmh)

    forecast_type = _forecast_type_from_z(z_raw)
    letter = TYPE_LETTERS[forecast_type]
    return FORECAST_TEXTS[forecast_type][language_index], forecast_type, letter


def _apply_northern_wind_correction(z_hp: float, direction_deg: float, bar_range: float) -> float:
    """Apply wind correction used by Negretti and Zambra implementation."""
    if 11.25 < direction_deg <= 33.75:
        return z_hp + 5 / 100 * bar_range
    if 33.75 < direction_deg <= 56.25:
        return z_hp + 4.6 / 100 * bar_range
    if 56.25 < direction_deg <= 78.75:
        return z_hp + 2 / 100 * bar_range
    if 78.75 < direction_deg <= 101.25:
        return z_hp - 0.5 / 100 * bar_range
    if 101.25 < direction_deg <= 123.75:
        return z_hp - 3.2 / 100 * bar_range
    if 123.75 < direction_deg <= 146.25:
        return z_hp - 5 / 100 * bar_range
    if 146.25 < direction_deg <= 168.75:
        return z_hp - 8.5 / 100 * bar_range
    if 168.75 < direction_deg <= 191.25:
        return z_hp - 11.2 / 100 * bar_range
    if 191.25 < direction_deg <= 213.75:
        return z_hp - 10 / 100 * bar_range
    if 213.75 < direction_deg <= 236.25:
        return z_hp - 6 / 100 * bar_range
    if 236.25 < direction_deg <= 258.75:
        return z_hp - 4.5 / 100 * bar_range
    if 258.75 < direction_deg <= 281.25:
        return z_hp - 3 / 100 * bar_range
    if 281.25 < direction_deg <= 303.75:
        return z_hp - 0.5 / 100 * bar_range
    if 303.75 < direction_deg <= 326.25:
        return z_hp + 1.5 / 100 * bar_range
    if 326.25 < direction_deg <= 348.75:
        return z_hp + 3 / 100 * bar_range
    if direction_deg > 348.75:
        return z_hp + 6 / 100 * bar_range
    return z_hp


def neg_zam_forecast(
    p0_hpa: float,
    pressure_change_3h: float,
    wind_direction_deg: float,
    wind_speed_kmh: float,
    is_northern_hemisphere: bool,
    language_index: int,
    now: datetime,
) -> tuple[str, int, str]:
    """Calculate Negretti and Zambra forecast text, raw number and letter."""
    bar_top = 1050.0
    bar_bottom = 950.0
    bar_range = bar_top - bar_bottom
    constant = bar_range / 22

    trend = pressure_trend_index(pressure_change_3h)
    z_hp = p0_hpa

    adjusted_direction = wind_direction_deg
    if not is_northern_hemisphere:
        adjusted_direction = (wind_direction_deg + 180) % 360

    if wind_speed_factor(wind_speed_kmh) == 1:
        z_hp = _apply_northern_wind_correction(z_hp, adjusted_direction, bar_range)

    if _is_summer(now, is_northern_hemisphere):
        if trend > 0:
            z_hp += 7 / 100 * bar_range
        elif trend < 0:
            z_hp -= 7 / 100 * bar_range

    if z_hp == bar_top:
        z_hp = bar_top - 1

    z_option = int(floor((z_hp - bar_bottom) / constant))
    prefix = ""
    if z_option < 0:
        z_option = 0
        prefix = EXCEPTIONAL_TEXT[language_index]
    elif z_option > 21:
        z_option = 21
        prefix = EXCEPTIONAL_TEXT[language_index]

    if trend > 0:
        z_num = RISE_OPT[z_option]
    elif trend < 0:
        z_num = FALL_OPT[z_option]
    else:
        z_num = STEADY_OPT[z_option]

    letter = forecast_letter_from_number(z_num)
    return prefix + FORECAST_TEXTS[z_num][language_index], z_num, letter


def _build_detail(
    forecast_code: int,
    is_night: bool,
    now: datetime,
    mapping: dict[int, tuple[int, int]],
    zambretti_variant: bool,
) -> dict[str, object]:
    """Build detail payload with rain probabilities, icons and time windows."""
    # The legacy template uses "+1" before mapping to card detail buckets.
    # Some paths can produce 26 while our maps are 1..25, so clamp explicitly.
    normalized_code = max(1, min(25, int(forecast_code)))
    forecast = mapping.get(normalized_code, (3, 3))

    if zambretti_variant:
        if forecast[0] == 0 and forecast[1] == 0:
            rain_prob = (0, 0)
        elif forecast[0] == 2 and forecast[1] == 1:
            rain_prob = (60, 10)
        elif forecast[0] == 1 and forecast[1] == 1:
            rain_prob = (30, 30)
        elif forecast[0] == 1 and forecast[1] == 0:
            rain_prob = (10, 0)
        elif forecast[0] == 1 and forecast[1] >= 2:
            rain_prob = (20, 60)
        elif forecast[0] == 2 and forecast[1] == 2:
            rain_prob = (50, 50)
        elif forecast[0] == 2 and forecast[1] > 2:
            rain_prob = (50, 70)
        elif forecast[0] >= 2 and forecast[1] < 2:
            rain_prob = (50, 10)
        else:
            rain_prob = (90, 90)
    else:
        if forecast[0] < 2 and forecast[1] < 2:
            rain_prob = (0, 0)
        elif forecast[0] == 1 and forecast[1] >= 2:
            rain_prob = (20, 60)
        elif forecast[0] == 2 and forecast[1] == 2:
            rain_prob = (50, 50)
        elif forecast[0] == 2 and forecast[1] > 2:
            rain_prob = (50, 70)
        else:
            rain_prob = (90, 90)

    daynight = 1 if is_night else 0
    icon_now = ICON_CONDITIONS[forecast[0]][daynight]
    icon_later = ICON_CONDITIONS[forecast[1]][daynight]

    first_delta = timedelta(hours=3)
    second_delta = timedelta(hours=9)
    first_time = now + first_delta
    second_time = now + second_delta

    return {
        "forecast": [forecast[0], forecast[1]],
        "rain_prob": [rain_prob[0], rain_prob[1]],
        "icons": (icon_now, icon_later),
        "first_time": [first_time.strftime("%H:%M"), round(first_delta.total_seconds() / 60, 2)],
        "second_time": [
            second_time.strftime("%H:%M"),
            round(second_delta.total_seconds() / 60, 2),
        ],
    }


def zambretti_detail(forecast_type: int, is_night: bool, now: datetime) -> dict[str, object]:
    """Return detailed values for Zambretti forecast card."""
    return _build_detail(
        forecast_code=forecast_type + 1,
        is_night=is_night,
        now=now,
        mapping=ZAMBRETTI_FORECAST_BY_CODE,
        zambretti_variant=True,
    )


def neg_zam_detail(z_number: int, is_night: bool, now: datetime) -> dict[str, object]:
    """Return detailed values for Negretti/Zam forecast card."""
    return _build_detail(
        forecast_code=z_number + 1,
        is_night=is_night,
        now=now,
        mapping=NEG_ZAM_FORECAST_BY_CODE,
        zambretti_variant=False,
    )


def short_temperature_forecast(
    temperature_c: float,
    temperature_change_1h: float,
    first_minutes: float,
    second_minutes: float,
) -> tuple[float | str, int]:
    """Return ultra short-term temperature forecast and interval selector."""
    if first_minutes > 0:
        forecast = round((temperature_change_1h / 60 * first_minutes) + temperature_c, 1)
        return forecast, 0
    if second_minutes > 0:
        forecast = round((temperature_change_1h / 60 * second_minutes) + temperature_c, 1)
        return forecast, 1
    return "unavailable", -1
