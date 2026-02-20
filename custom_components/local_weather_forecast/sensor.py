"""Sensor platform for Local Weather Forecast integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfPressure, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import LocalWeatherForecastCoordinator, LocalWeatherForecastData


@dataclass(frozen=True, kw_only=True)
class LocalForecastSensorDescription(SensorEntityDescription):
    """Describes Local Weather Forecast sensor entities."""

    data_key: str


SENSOR_DESCRIPTIONS: tuple[LocalForecastSensorDescription, ...] = (
    LocalForecastSensorDescription(
        key="main",
        name="Local forecast",
        data_key="main",
        icon="mdi:weather-cloudy-clock",
    ),
    LocalForecastSensorDescription(
        key="zambretti_detail",
        name="Local forecast zambretti detail",
        data_key="zambretti_detail",
        icon="mdi:weather-partly-rainy",
    ),
    LocalForecastSensorDescription(
        key="neg_zam_detail",
        name="Local forecast neg_zam detail",
        data_key="neg_zam_detail",
        icon="mdi:weather-partly-snowy-rainy",
    ),
    LocalForecastSensorDescription(
        key="pressure",
        name="Local forecast pressure",
        data_key="pressure",
        device_class=SensorDeviceClass.ATMOSPHERIC_PRESSURE,
        native_unit_of_measurement=UnitOfPressure.HPA,
    ),
    LocalForecastSensorDescription(
        key="temperature",
        name="Local forecast temperature",
        data_key="temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    LocalForecastSensorDescription(
        key="pressure_change",
        name="Local forecast pressurechange",
        data_key="pressure_change",
        native_unit_of_measurement=UnitOfPressure.HPA,
        icon="mdi:chart-line",
    ),
    LocalForecastSensorDescription(
        key="temperature_change",
        name="Local forecast temperaturechange",
        data_key="temperature_change",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        icon="mdi:thermometer-lines",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Local Weather Forecast sensors."""
    coordinator: LocalWeatherForecastCoordinator = entry.runtime_data

    async_add_entities(
        LocalForecastSensor(coordinator, entry, description) for description in SENSOR_DESCRIPTIONS
    )


class LocalForecastSensor(CoordinatorEntity[LocalWeatherForecastCoordinator], SensorEntity):
    """Representation of a Local Weather Forecast sensor."""

    entity_description: LocalForecastSensorDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: LocalWeatherForecastCoordinator,
        entry: ConfigEntry,
        description: LocalForecastSensorDescription,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Local Weather Forecast",
            manufacturer="Community",
            model="Zambretti/Negretti",
        )

    @property
    def native_value(self) -> Any:
        """Return sensor state."""
        data = self.coordinator.data
        if data is None:
            return None

        if self.entity_description.data_key == "main":
            return data.main_state
        if self.entity_description.data_key == "zambretti_detail":
            return data.zambretti_state
        if self.entity_description.data_key == "neg_zam_detail":
            return data.neg_zam_state
        if self.entity_description.data_key == "pressure":
            return data.pressure
        if self.entity_description.data_key == "temperature":
            return data.temperature
        if self.entity_description.data_key == "pressure_change":
            return data.pressure_change
        if self.entity_description.data_key == "temperature_change":
            return data.temperature_change
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return state attributes."""
        data: LocalWeatherForecastData | None = self.coordinator.data
        if data is None:
            return None

        # Keep attribute payloads shaped like the original template sensors
        # so existing Lovelace YAML cards keep working without migration.
        if self.entity_description.data_key == "main":
            return data.main_attributes
        if self.entity_description.data_key == "zambretti_detail":
            return data.zambretti_attributes
        if self.entity_description.data_key == "neg_zam_detail":
            return data.neg_zam_attributes
        return None
