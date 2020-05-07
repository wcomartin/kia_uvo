"""The Kia Uvo integration."""
import asyncio
from datetime import timedelta

import voluptuous as vol

from homeassistant import bootstrap
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.dispatcher import (
    async_dispatcher_connect,
    async_dispatcher_send,
)
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD, CONF_PIN

from .const import DOMAIN, CONF_VEHICLE_ID, VEHICLE_ACCOUNT, VEHICLE_LISTENER, FORCE_VEHICLE_LISTENER, LOGGER, TOPIC_UPDATE

from KiaUvo import KiaUvo, InvalidAuthException, NoVehicleException

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS = ["binary_sensor"]

DEFAULT_SCAN_INTERVAL = timedelta(minutes=1)
FORCE_SCAN_INTERVAL = timedelta(minutes=60)

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass: HomeAssistant, config):
    """Set up the Kia Uvo component."""
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    # hass.data[DOMAIN] = {VEHICLE_ACCOUNTS: [], VEHICLE_LISTENER: {}, FORCE_VEHICLE_LISTENER: {}}

    # async def async_handle_start_engine(call):
    #     """Handle the service call 'start_engine'"""
    #     vehicle_id = call.data.get("vehicle_id")
    #     preset = call.data.get("preset")
    #     print(vehicle_id)
    #     print(preset)
    #
    #     account = next(
    #         entry[VEHICLE_ACCOUNT]
    #         for entry in hass.data[DOMAIN].values()
    #         if entry[VEHICLE_ACCOUNT].data[CONF_VEHICLE_ID] == vehicle_id)
    #
    #     await hass.async_add_executor_job(account.kia.login)
    #     await hass.async_add_executor_job(account.kia.verify_token)
    #     await hass.async_add_executor_job(account.kia.lock_vehicle)
    #
    # async def async_handle_stop_engine(call):
    #     """Handle the service call 'stop_engine'"""
    #     vehicle_id = call.data.get("vehicle_id")
    #     print(vehicle_id)
    #
    #     account = next(
    #         entry[VEHICLE_ACCOUNT]
    #         for entry in hass.data[DOMAIN].values()
    #         if entry[VEHICLE_ACCOUNT].data[CONF_VEHICLE_ID] == vehicle_id)
    #
    #     await hass.async_add_executor_job(account.kia.login)
    #     await hass.async_add_executor_job(account.kia.verify_token)
    #     await hass.async_add_executor_job(account.kia.stop_vehicle)

    async def async_handle_lock(call):
        """Handle the service call 'lock'"""
        vehicle_id = call.data.get("vehicle_id")
        print(vehicle_id)

        account = next(
            entry[VEHICLE_ACCOUNT]
            for entry in hass.data[DOMAIN].values()
            if entry[VEHICLE_ACCOUNT].data[CONF_VEHICLE_ID] == vehicle_id)

        await hass.async_add_executor_job(account.kia.login)
        await hass.async_add_executor_job(account.kia.verify_token)
        await hass.async_add_executor_job(account.kia.lock_vehicle)

    async def async_handle_unlock(call):
        """Handle the service call 'unlock'"""
        vehicle_id = call.data.get("vehicle_id")
        print(vehicle_id)

        account = next(
            entry[VEHICLE_ACCOUNT]
            for entry in hass.data[DOMAIN].values()
            if entry[VEHICLE_ACCOUNT].data[CONF_VEHICLE_ID] == vehicle_id)

        await hass.async_add_executor_job(account.kia.login)
        await hass.async_add_executor_job(account.kia.verify_token)
        await hass.async_add_executor_job(account.kia.unlock_vehicle)

    async def async_handle_force_update_vehicle(call):
        """Handle the service call 'unlock'"""
        vehicle_id = call.data.get("vehicle_id")
        print(vehicle_id)

        account = next(
            entry[VEHICLE_ACCOUNT]
            for entry in hass.data[DOMAIN].values()
            if entry[VEHICLE_ACCOUNT].data[CONF_VEHICLE_ID] == vehicle_id)

        await hass.async_add_executor_job(account.kia.login)
        await hass.async_add_executor_job(account.kia.verify_token)
        await hass.async_add_executor_job(account.kia.async_force_vehicle_update)

    # hass.services.async_register(DOMAIN, "start_engine", async_handle_start_engine)
    # hass.services.async_register(DOMAIN, "stop_engine", async_handle_stop_engine)
    #
    hass.services.async_register(DOMAIN, "lock", async_handle_lock)
    hass.services.async_register(DOMAIN, "unlock", async_handle_unlock)
    hass.services.async_register(DOMAIN, "force_update_vehicle", async_handle_force_update_vehicle)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Kia Uvo from a config entry."""

    data = {
        VEHICLE_ACCOUNT: KiaUvoData(hass, entry),
        VEHICLE_LISTENER: {},
        FORCE_VEHICLE_LISTENER: {}
    }

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    async def refresh(event_time):
        """Refresh data from Kia UVO."""
        await data[VEHICLE_ACCOUNT].async_update()

    async def force_vehicle_update(event_time):
        """Send request to vehicle for update"""
        await data[VEHICLE_ACCOUNT].async_force_vehicle_update()

    data[VEHICLE_LISTENER] = async_track_time_interval(
        hass, refresh, DEFAULT_SCAN_INTERVAL
    )

    data[FORCE_VEHICLE_LISTENER] = async_track_time_interval(
        hass, force_vehicle_update, FORCE_SCAN_INTERVAL
    )

    hass.data[DOMAIN][entry.entry_id] = data

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class KiaUvoEntity(Entity):

    def __init__(self, hass, config_entry):
        self._hass = hass
        self._config_entry = config_entry
        self.topic_update = TOPIC_UPDATE.format(config_entry.data[CONF_VEHICLE_ID])

    async def async_added_to_hass(self):
        """Register callbacks."""

        @callback
        def update():
            """Update the state."""
            self.update_from_latest_data()
            self.async_write_ha_state()

        self.async_on_remove(
            async_dispatcher_connect(self._hass, self.topic_update, update)
        )

        self.update_from_latest_data()

    @callback
    def update_from_latest_data(self):
        """Update the entity from the latest data."""
        raise NotImplementedError


class KiaUvoData:

    def __init__(self, hass, config_entry):
        """Initialize"""
        self._hass = hass
        self._config_entry = config_entry
        self.data = config_entry.data
        self.topic_update = TOPIC_UPDATE.format(config_entry.data[CONF_VEHICLE_ID])
        self.kia = KiaUvo(self.data[CONF_USERNAME], self.data[CONF_PASSWORD])
        self.kia.select_vehicle(self.data[CONF_VEHICLE_ID], self.data[CONF_PIN])
        self.vehicle_data = {}

    async def async_update(self):
        try:
            await self._hass.async_add_executor_job(self.kia.login)
            await self._hass.async_add_executor_job(self.kia.verify_token)

            self.vehicle_data = await self._hass.async_add_executor_job(self.kia.get_vehicle_status)
        except Exception:
            self.vehicle_data = {}

        LOGGER.debug("Received new vehicle data")
        async_dispatcher_send(self._hass, self.topic_update)

    async def async_force_vehicle_update(self):
        try:
            await self._hass.async_add_executor_job(self.kia.login)
            await self._hass.async_add_executor_job(self.kia.verify_token)

            # Force update from vehicle
            await self._hass.async_add_executor_job(self.kia.request_vehicle_update)

            self.vehicle_data = await self._hass.async_add_executor_job(self.kia.get_vehicle_status)
        except Exception:
            self.vehicle_data = {}

