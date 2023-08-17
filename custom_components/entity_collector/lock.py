import logging

from .const import *
import re
from homeassistant.components.lock import *

from .device import EntityBase, async_setup

from homeassistant.const import *

_LOGGER = logging.getLogger(__name__)

PLATFORM = "lock"

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    await async_setup(hass, PLATFORM, EntityCollector, config_entry, async_add_devices)

class EntityCollector(EntityBase, LockEntity):

    # platform property #############################################################################
    @property
    def changed_by(self) -> str | None:
        return self._attributes.get(ATTR_CHANGED_BY)

    @property
    def code_format(self) -> str | None:
        return self._attributes.get(ATTR_CODE_FORMAT)
    
    @property
    def is_locked(self) -> bool | None:
        return self._state == STATE_LOCKED

    @property
    def is_locking(self) -> bool | None:
        return self._state == STATE_LOCKING

    @property
    def is_unlocking(self) -> bool | None:
        return self._state == STATE_UNLOCKING

    @property
    def is_jammed(self) -> bool | None:
        return self._state == STATE_JAMMED

    @property
    def supported_features(self) -> int | None:
        return self._attributes.get(ATTR_SUPPORTED_FEATURES) if self._attributes.get(ATTR_SUPPORTED_FEATURES) != None else LockEntityFeature.OPEN

    # method ########################################################################################
    def lock(self, **kwargs: Any) -> None:
        self.hass.services.call('lock', 'lock', {
                                        "entity_id": self._origin_entity}, False)

    def unlock(self, **kwargs: Any) -> None:
        self.hass.services.call('lock', 'unlock', {
                                        "entity_id": self._origin_entity}, False)

    def open(self, **kwargs: Any) -> None:
        self.hass.services.call('lock', 'open', {
                                        "entity_id": self._origin_entity}, False)

