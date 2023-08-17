

DOMAIN = "entity_collector"
NAME = "Entity Collector"
VERSION = "1.0.0"

#ENTITY_ID_FORMAT = DOMAIN + ".{}"

CONF_DEVICE_NAME = "device_name"
CONF_ORIGIN_ENTITY = "origin_entity"
CONF_ENTITIES = "entities"
CONF_ADD_ANODHER = "add_another"
CONF_NAME = "name"


ENTITY_TYPE = {
    "sensor" : { "sensor", },
    "binary_sensor" : { "binary_sensor", },
    "switch" : { "switch", "input_boolean" },
    "number" : { "number", "input_number" },
    "button" : { "button" },
    "fan" : { "fan" },
    "cover": { "cover" },
    "climate": { "climate" },
    "select": { "select", "input_select" },
    "light": { "light" },
    "text": { "text", "input_text" },
    "lock": { "lock" },
    "camera": { "camera" },
    "media_player": { "media_player" },
}
