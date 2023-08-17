import logging

from .const import *
import re
from homeassistant.components.select import *

from .device import EntityBase, async_setup

from homeassistant.const import *

_LOGGER = logging.getLogger(__name__)

PLATFORM = "select"

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    await async_setup(hass, PLATFORM, EntityCollector, config_entry, async_add_devices)

class EntityCollector(EntityBase, SelectEntity):

    # platform property ##############################################################################
    @property
    def current_option(self) -> str | None:
        return self._attributes.get(ATTR_OPTION)
    
    @property
    def options(self) -> list[str]:
        return self._attributes.get(ATTR_OPTIONS)

    # method #########################################################################################
    def select_option(self, option: str) -> None:
        if re.search("^input_select.", self._origin_entity):
            self.hass.services.call('input_select', 'select_option', {
                                            "entity_id": self._origin_entity,  ATTR_OPTION: option }, False)
        elif re.search("^select.", self._origin_entity):
            self.hass.services.call('select', 'select_option', {
                                            "entity_id": self._origin_entity,  ATTR_OPTION: option }, False)