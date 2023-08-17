import logging

from .const import *
import re
from homeassistant.components.button import ButtonEntity

from .device import EntityBase, async_setup

from homeassistant.const import *

_LOGGER = logging.getLogger(__name__)

PLATFORM = "button"

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    await async_setup(hass, PLATFORM, EntityCollector, config_entry, async_add_devices)

class EntityCollector(EntityBase, ButtonEntity):

    # platform property ##############################################################################

    # method #########################################################################################
    def press(self):
        """Update the state."""
        self.hass.services.call('button', 'press', {
                                        "entity_id": self._origin_entity}, False)
