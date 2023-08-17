import logging

from .const import *
import re
from homeassistant.components.cover import CoverEntity, ATTR_CURRENT_POSITION, ATTR_CURRENT_TILT_POSITION, ATTR_POSITION, ATTR_TILT_POSITION, STATE_CLOSING, STATE_CLOSED,CoverEntityFeature

from .device import EntityBase, async_setup

from homeassistant.const import *

_LOGGER = logging.getLogger(__name__)

PLATFORM = "cover"

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    await async_setup(hass, PLATFORM, EntityCollector, config_entry, async_add_devices)

class EntityCollector(EntityBase, CoverEntity):

    # platform property #############################################################################
    @property
    def current_cover_position(self) -> int | None:
        return self._attributes.get(ATTR_CURRENT_POSITION)
    
    @property
    def current_cover_tilt_position(self) -> int | None:
        return self._attributes.get(ATTR_CURRENT_TILT_POSITION)
    
    @property
    def is_opening(self) -> bool | None:
        return self._state == STATE_OPENING
    
    @property
    def is_closing(self) -> bool | None:
        return self._state == STATE_CLOSING

    @property
    def is_closed(self) -> bool | None:
        return self._state == STATE_CLOSED

    @property
    def supported_features(self) -> int | None:
        return self._attributes.get("supported_features") if self._attributes.get("supported_features") != None else CoverEntityFeature.OPEN

    # method ########################################################################################
    def open_cover(self, **kwargs):
        """Open the cover."""
        self.hass.services.call('cover', 'open_cover', {
                                "entity_id": self._origin_entity}, False)

    def close_cover(self, **kwargs):
        """Close cover."""
        self.hass.services.call('cover', 'close_cover', {
                                "entity_id": self._origin_entity}, False)

    def set_cover_position(self, **kwargs):
        """Move the cover to a specific position."""
        self.hass.services.call('cover', 'close_cover', {
                                "entity_id": self._origin_entity, "position" : kwargs[ATTR_POSITION] }, False)
    def stop_cover(self, **kwargs):
        """Stop the cover."""
        self.hass.services.call('cover', 'stop_cover', {
                                "entity_id": self._origin_entity}, False)

    def open_cover_tilt(self, **kwargs):
        """Open the cover tilt."""
        self.hass.services.call('cover', 'open_cover_tilt', {
                                "entity_id": self._origin_entity}, False)

    def close_cover_tilt(self, **kwargs):
        """Close the cover tilt."""
        self.hass.services.call('cover', 'close_cover_tilt', {
                                "entity_id": self._origin_entity}, False)

    def set_cover_tilt_position(self, **kwargs):
        """Move the cover tilt to a specific position."""
        self.hass.services.call('cover', 'set_cover_tilt_position', {
                                "entity_id": self._origin_entity, "position" : kwargs[ATTR_POSITION] }, False)

    def stop_cover_tilt(self, **kwargs):
        """Stop the cover."""
        self.hass.services.call('cover', 'stop_cover_tilt', {
                                "entity_id": self._origin_entity}, False)
