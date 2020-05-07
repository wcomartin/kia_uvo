"""Constants for the Kia Uvo integration."""
import logging

__version__ = "0.1.8"

DOMAIN = "kia_uvo"
LOGGER = logging.getLogger(__package__)

CONF_VEHICLE_ID = "vehicle_id"
VEHICLE_DATA = "vehicle_data"
VEHICLE_ACCOUNT = "vehicle_account"
VEHICLE_LISTENER = "vehicle_listener"
FORCE_VEHICLE_LISTENER = "force_vehicle_listener"

TOPIC_UPDATE = f"kiauvo_update_{0}"
