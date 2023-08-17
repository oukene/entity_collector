import logging

from .const import *
import re
from homeassistant.components.fan import *

from .device import EntityBase, async_setup

from homeassistant.const import *

_LOGGER = logging.getLogger(__name__)

PLATFORM = "fan"

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    await async_setup(hass, PLATFORM, EntityCollector, config_entry, async_add_devices)

class EntityCollector(EntityBase, FanEntity):

    # platform property #############################################################################
    @property
    def is_on(self) -> bool | None:
        if self._state == "on":
            return True
        elif self._state == "off":
            return False

    @property
    def current_direction(self) -> str | None:
        return self._attributes.get(ATTR_DIRECTION)

    @property
    def oscillate(self, oscillating: bool) -> None:
        return self._attributes.get(ATTR_OSCILLATING)

    @property
    def percentage(self) -> int | None:
        return self._attributes.get(ATTR_PERCENTAGE)

    @property
    def percentage_step(self) -> float:
        return self._attributes.get(ATTR_PERCENTAGE_STEP)

    @property
    def preset_modes(self) -> list[str] | None:
        return self._attributes.get(ATTR_PRESET_MODES)
    
    @property
    def preset_mode(self) -> str | None:
        return self._attributes.get(ATTR_PRESET_MODE)

    @property
    def supported_features(self) -> int | None:
        return self._attributes.get("supported_features") if self._attributes.get("supported_features") != None else FanEntityFeature.SET_SPEED

    # method ########################################################################################

    async def async_turn_on(self, percentage: int | None = None, preset_mode: str | None = None, **kwargs: Any) -> None:
        return await self.hass.services.async_call('fan', 'turn_on', {
                                        "entity_id": self._origin_entity}, False)

    def turn_on(self, **kwargs) -> None:
        return self.hass.services.call('fan', 'turn_on', {
                                        "entity_id": self._origin_entity}, False)

    async def async_turn_off(self, **kwargs: Any) -> None:
        return await self.hass.services.async_call('fan', 'turn_off', {
                                        "entity_id": self._origin_entity}, False)

    def turn_off(self, **kwargs) -> None:
        return self.hass.services.call('fan', 'turn_off', {
                                        "entity_id": self._origin_entity}, False)

    async def async_set_direction(self, direction: str) -> None:
        return await self.hass.services.async_call('fan', 'set_direction', {
                                        "entity_id": self._origin_entity, "direction" : direction }, False)

    def set_direction(self, direction: str) -> None:
        return self.hass.services.call('fan', 'set_direction', {
                                        "entity_id": self._origin_entity, "direction" : direction }, False)
    
    async def async_set_preset_mode(self, preset_mode: str) -> None:
        return await self.hass.services.async_call('fan', 'set_preset_mode', {
                                        "entity_id": self._origin_entity, "preset_mode" : preset_mode }, False)
        

    def set_preset_mode(self, preset_mode: str) -> None:
        """Set the preset mode of the fan."""
        return self.hass.services.call('fan', 'set_preset_mode', {
                                        "entity_id": self._origin_entity, "preset_mode" : preset_mode }, False)

    async def async_set_percentage(self, percentage: int) -> None:
        return await self.hass.services.async_call('fan', 'set_percentage', {
                                        "entity_id": self._origin_entity, "percentage" : percentage }, False)

    def set_percentage(self, percentage: int) -> None:
        """Set the speed percentage of the fan."""
        return self.hass.services.call('fan', 'set_percentage', {
                                        "entity_id": self._origin_entity, "percentage" : percentage }, False)

    async def async_oscillate(self, oscillating: bool) -> None:
        return await self.hass.services.async_call('fan', 'oscillate', {
                                        "entity_id": self._origin_entity, "oscillating" : oscillating }, False)

    def oscillate(self, oscillating: bool) -> None:
        """Oscillate the fan."""
        return self.hass.services.call('fan', 'oscillate', {
                                        "entity_id": self._origin_entity, "oscillating" : oscillating }, False)