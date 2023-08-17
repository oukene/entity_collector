import logging

from .const import *
import re
from homeassistant.components.switch import *

from .device import EntityBase, async_setup

from homeassistant.const import *

_LOGGER = logging.getLogger(__name__)

PLATFORM = "switch"

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    await async_setup(hass, PLATFORM, EntityCollector, config_entry, async_add_devices)

class EntityCollector(EntityBase, SwitchEntity):

    # platform property #############################################################################
    @property
    def is_on(self) -> bool | None:
        if self._state == "on":
            return True
        elif self._state == "off":
            return False

    # method ########################################################################################

    def turn_on(self, **kwargs) -> None:
        self.hass.services.call('homeassistant', 'turn_on', {
                                        "entity_id": self._origin_entity}, False)

    def turn_off(self, **kwargs) -> None:
        self.hass.services.call('homeassistant', 'turn_off', {
                                        "entity_id": self._origin_entity}, False)

