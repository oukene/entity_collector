import logging

from .const import *
import re
from homeassistant.components.climate import *

from homeassistant.components.climate.const import ClimateEntityFeature


from .device import EntityBase, async_setup

from homeassistant.const import *

_LOGGER = logging.getLogger(__name__)

PLATFORM = "climate"

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    await async_setup(hass, PLATFORM, EntityCollector, config_entry, async_add_devices)

class EntityCollector(EntityBase, ClimateEntity):

    # platform property #############################################################################
    @property
    def temperature_unit(self) -> str:
        return self.hass.config.units.temperature_unit

    @property
    def precision(self) -> float:
        """Return the precision of the system."""
        if hasattr(self, "_attr_precision"):
            return self._attr_precision
        if self.hass.config.units.temperature_unit == UnitOfTemperature.CELSIUS:
            return PRECISION_TENTHS
        return PRECISION_WHOLE

    @property
    def current_temperature(self) -> float | None:
        return self._attributes.get(ATTR_CURRENT_TEMPERATURE)

    @property
    def current_humidity(self) -> int | None:
        return self._attributes.get(ATTR_CURRENT_HUMIDITY)

    @property
    def target_temperature(self) -> float | None:
        return self._attributes.get(ATTR_TEMPERATURE)

    @property
    def target_temperature_high(self) -> float | None:
        return self._attributes.get(ATTR_TARGET_TEMP_HIGH)
    
    @property
    def target_temperature_low(self) -> float | None:
        return self._attributes.get(ATTR_TARGET_TEMP_LOW)

    @property
    def target_temperature_step(self) -> float | None:
        return self._attributes.get(ATTR_TARGET_TEMP_STEP)
    
    @property
    def target_humidity(self) -> int | None:
        return self._attributes.get(ATTR_HUMIDITY)

    @property
    def max_temp(self) -> float:
        return self._attributes.get(ATTR_MAX_TEMP)

    @property
    def min_temp(self) -> float:
        return self._attributes.get(ATTR_MIN_TEMP)

    @property
    def max_humidity(self) -> int:
        return self._attributes.get(ATTR_MAX_HUMIDITY)

    @property
    def min_humidity(self) -> int:
        return self._attributes.get(ATTR_MIN_HUMIDITY)

    @property
    def hvac_mode(self) -> HVACMode | None:
        return self._attributes.get(ATTR_HVAC_MODE)

    @property
    def hvac_action(self) -> HVACAction | None:
        return self._attributes.get(ATTR_HVAC_ACTION)

    @property
    def hvac_modes(self) -> list[HVACMode]:
        return self._attributes.get(ATTR_HVAC_MODES)

    @property
    def preset_mode(self) -> str | None:
        return self._attributes.get(ATTR_PRESET_MODE)

    @property
    def preset_modes(self) -> list[str] | None:
        return self._attributes.get(ATTR_PRESET_MODES)

    @property
    def fan_mode(self) -> str | None:
        return self._attributes.get(ATTR_FAN_MODE)
    
    @property
    def fan_modes(self) -> list[str] | None:
        return self._attributes.get(ATTR_FAN_MODES)

    @property
    def swing_mode(self) -> str | None:
        return self._attributes.get(ATTR_SWING_MODE)

    @property
    def swing_modes(self) -> list[str] | None:
        return self._attributes.get(ATTR_SWING_MODES)

    @property
    def is_aux_heat(self) -> bool | None:
        return self._attributes.get(ATTR_AUX_HEAT)
    
    @property
    def supported_features(self) -> int | None:
        return self._attributes.get(ATTR_SUPPORTED_FEATURES) if self._attributes.get(ATTR_SUPPORTED_FEATURES) != None else (ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.FAN_MODE)

    # method ########################################################################################
    def set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""
        self.hass.services.call('climate', 'set_hvac_mode', {
                                        "entity_id": self._origin_entity, ATTR_HVAC_MODE : hvac_mode }, False)

    def set_preset_mode(self, preset_mode):
        """Set new target preset mode."""
        self.hass.services.call('climate', 'set_preset_mode', {
                                        "entity_id": self._origin_entity, ATTR_PRESET_MODE : preset_mode }, False)

    def set_fan_mode(self, fan_mode):
        """Set new target fan mode."""
        self.hass.services.call('climate', 'set_fan_mode', {
                                        "entity_id": self._origin_entity, ATTR_FAN_MODE : fan_mode }, False)

    def set_humidity(self, humidity):
        """Set new target humidity."""
        self.hass.services.call('climate', 'set_humidity', {
                                        "entity_id": self._origin_entity, ATTR_HUMIDITY : humidity }, False)

    def set_swing_mode(self, swing_mode):
        """Set new target swing operation."""
        self.hass.services.call('climate', 'set_swing_mode', {
                                        "entity_id": self._origin_entity, ATTR_SWING_MODE : swing_mode }, False)
    

    def set_temperature(self, **kwargs):
        """Set new target temperature."""
        #for key, value in kwargs.items():
        #    _LOGGER.error("turn_on key : " + str(key) + ", value : " + str(value))
        self.hass.services.call('climate', 'set_temperature', {
                                        "entity_id": self._origin_entity, ATTR_TEMPERATURE : kwargs[ATTR_TEMPERATURE] }, False)

    def turn_on(self):
        """Turn auxiliary heater on."""
        self.hass.services.call('climate', 'turn_on', {
                                        "entity_id": self._origin_entity}, False)

    def turn_off(self):
        """Turn auxiliary heater off."""
        self.hass.services.call('climate', 'turn_off', {
                                        "entity_id": self._origin_entity}, False)