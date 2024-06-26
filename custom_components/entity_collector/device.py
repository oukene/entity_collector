import asyncio
from .const import *
from homeassistant.helpers.entity import Entity

import logging
import re
from homeassistant.const import (
    STATE_UNKNOWN, STATE_UNAVAILABLE,
)

from .const import *
from homeassistant.helpers.entity import async_generate_entity_id
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.core import Event, EventStateChangedData, callback

from homeassistant.const import *

ENTITY_ID_FORMAT = DOMAIN + ".{}"

_LOGGER = logging.getLogger(__name__)

def _is_valid_state(state) -> bool:
    return state and state.state != STATE_UNKNOWN and state.state != STATE_UNAVAILABLE

async def async_setup(hass, platform, entity_type, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""

    hass.data[DOMAIN][config_entry.entry_id]["listener"] = []
    
    _LOGGER.debug("data : %s", config_entry.data)
    _LOGGER.debug("options : %s", config_entry.options)
    device = hass.data[DOMAIN][config_entry.entry_id]["device"]

    new_devices = []

    if config_entry.options.get(CONF_ENTITIES) != None:
        for key in config_entry.options.get(CONF_ENTITIES):
            _LOGGER.debug("key : %s", key)
            entity = config_entry.options[CONF_ENTITIES][key]
            for e in ENTITY_TYPE[platform]:
                if re.search("^" + e, key):
                    _LOGGER.debug("PLATFORM : %s, add entity : %s, entity : %s", platform, entity, entity)
                    new_devices.append(
                        entity_type(
                            hass,
                            config_entry.entry_id,
                            device,
                            entity[CONF_NAME],
                            entity[CONF_ORIGIN_ENTITY],
                        )
                    )
                    continue

        if new_devices:
            async_add_devices(new_devices)

class Device:
    """Dummy roller (device for HA) for Hello World example."""

    def __init__(self, name, config):
        """Init dummy roller."""
        self._id = f"{name}_{config.entry_id}"
        self._name = name
        self._callbacks = set()
        self._loop = asyncio.get_event_loop()
        self.firmware_version = VERSION
        self.model = "astar"
        self.manufacturer = "astar"

    @property
    def device_id(self):
        """Return ID for roller."""
        return self._id

    @property
    def name(self):
        return self._name

    def register_callback(self, callback):
        """Register callback, called when Roller changes state."""
        self._callbacks.add(callback)

    def remove_callback(self, callback):
        """Remove previously registered callback."""
        self._callbacks.discard(callback)

    # In a real implementation, this library would call it's call backs when it was
    # notified of any state changeds for the relevant device.
    async def publish_updates(self):
        """Schedule call all registered callbacks."""
        for callback in self._callbacks:
            callback()

    def publish_updates(self):
        """Schedule call all registered callbacks."""
        for callback in self._callbacks:
            callback()



class EntityBase(Entity):

    should_poll = False

    @property
    def device_info(self):
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, self._device.device_id)},
            "name": self._device.name,
            "sw_version": self._device.firmware_version,
            "model": self._device.model,
            "manufacturer": self._device.manufacturer
        }

    @property
    def available(self) -> bool:
        """Return True if roller and hub is available."""
        return True

    async def async_added_to_hass(self):
        """Run when this Entity has been added to HA."""
        self._device.register_callback(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """Entity being removed from hass."""
        self._device.remove_callback(self.async_write_ha_state)


    def __init__(self, hass, entry_id, device, entity_name, origin_entity):
        """Initialize the sensor."""
        super().__init__()
        self._device = device
        self.hass = hass
        self._origin_entity = origin_entity

        self.entity_id = async_generate_entity_id(
            ENTITY_ID_FORMAT, "{}_{}".format(self._device.name, entity_name), hass=hass)
        _LOGGER.debug("entity_id : %s", self.entity_id)
        self._name = "{}".format(entity_name)
        self._state = None
        self._attributes = {}

        self._unique_id = self.entity_id
        self._device = device

        hass.data[DOMAIN][entry_id]["listener"].append(async_track_state_change_event(
            self.hass, origin_entity, self.entity_listener))
        new_state = self.hass.states.get(origin_entity)
        old_state = self.hass.states.get(self.entity_id)
        _LOGGER.debug("origin entity state - " + str(new_state))

        self.entity_listener(origin_entity, old_state, new_state)

        self._device.publish_updates()

    @callback  # type: ignore[misc]
    def _state_changed_event(self, event: Event) -> None:
        """state change event."""
        self.entity_listener(event.data.get("entity_id"), event.data.get("old_state"), event.data.get("new_state"))

    def entity_listener(self, entity, old_state, new_state):
        _LOGGER.debug("call entity listener2")
        if _is_valid_state(new_state):
            self._attributes = new_state.attributes.copy()
            _LOGGER.debug("attributes : " + str(self._attributes))
            self._attributes[CONF_ORIGIN_ENTITY] = self._origin_entity
            self._state = new_state.state
            _LOGGER.debug("new_state.state : " + str(new_state.state))
            self._device.publish_updates()

    # default property ###############################################################################################
    """Sensor Properties"""
    @property
    def has_entity_name(self) -> bool:
        return True

    @property
    def assumed_state(self) -> bool:
        return self._attributes[ATTR_ASSUMED_STATE] if self._attributes.get(ATTR_ASSUMED_STATE) != None else None

    @property
    def device_class(self):
        return self._attributes[ATTR_DEVICE_CLASS] if self._attributes.get(ATTR_DEVICE_CLASS) != None else None

    @property
    def native_unit_of_measurement(self):
        """Return the unit_of_measurement of the device."""
        return self._attributes[ATTR_UNIT_OF_MEASUREMENT] if self._attributes.get(ATTR_UNIT_OF_MEASUREMENT) != None else None

    @property
    def extra_state_attributes(self):
        """Return entity specific state attributes."""
        return self._attributes

    @property
    def entity_picture(self) -> str | None:
        return self._attributes[ATTR_ENTITY_PICTURE] if self._attributes.get(ATTR_ENTITY_PICTURE) != None else None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self) -> str | None:
        return super().icon

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        if self._unique_id is not None:
            return self._unique_id

    @property
    def state(self):
        return self._state