"""Config flow for Kia Uvo integration."""
from typing import Optional
import logging

import voluptuous as vol

from homeassistant import core, config_entries, exceptions
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD, CONF_PIN
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, CONF_VEHICLE_ID

from KiaUvo import KiaUvo, InvalidAuthException, NoVehicleException

_LOGGER = logging.getLogger(__name__)


class DomainConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Kia Uvo."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize flow."""
        self.auth_info = None
        self.vehicle_info = None
        self.kia = None
        self.vehicles = []

    async def async_step_user(self, user_input: Optional[ConfigType] = None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                self.auth_info = await self.validate_authentication(user_input)
                return await self.async_step_vehicle()
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str
            }),
            errors=errors,
        )

    async def async_step_vehicle(self, user_input=None):

        errors = {}
        if user_input is not None:
            try:
                self.vehicle_info = await self.validate_vehicle(user_input)
                return await self.async_create()
            except InvalidPin:
                errors["base"] = "invalid_pin"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        self.vehicles = await self.hass.async_add_executor_job(self.kia.get_vehicle_list)
        vehicle_names = [x.vehicle["nickName"] for x in self.vehicles]

        return self.async_show_form(
            step_id="vehicle",
            data_schema=vol.Schema({
                vol.Required(CONF_VEHICLE_ID): vol.In(vehicle_names),
                vol.Required(CONF_PIN): str
            }),
            errors=errors
        )

    async def validate_authentication(self, user_input):
        """Validate the user input allows us to connect.

        Data has the keys from DATA_SCHEMA with values provided by the user.
        """
        self.kia = KiaUvo(user_input[CONF_USERNAME], user_input[CONF_PASSWORD])
        await self.hass.async_add_executor_job(self.kia.login)

        try:
            await self.hass.async_add_executor_job(self.kia.verify_token)
        except InvalidAuthException:
            raise InvalidAuth

        # Return some info we want to store in the config entry.
        return user_input

    async def validate_vehicle(self, user_input):

        vehicle = next((x for x in self.vehicles if x.vehicle["nickName"] == user_input[CONF_VEHICLE_ID]), None)

        return {CONF_VEHICLE_ID: vehicle.vehicle["vehicleId"], CONF_PIN: user_input[CONF_PIN], "vehicle": vehicle}

    async def async_create(self):
        await self.async_set_unique_id(self.vehicle_info[CONF_VEHICLE_ID])
        self._abort_if_unique_id_configured()
        data = {
            CONF_USERNAME: self.auth_info[CONF_USERNAME],
            CONF_PASSWORD: self.auth_info[CONF_PASSWORD],
            CONF_VEHICLE_ID: self.vehicle_info[CONF_VEHICLE_ID],
            CONF_PIN: self.vehicle_info[CONF_PIN],
        }
        title = f'Kia {self.vehicle_info["vehicle"].vehicle["modelName"]} ({self.vehicle_info["vehicle"].vehicle["nickName"]})'
        return self.async_create_entry(title=title, data=data)

class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is invalid auth."""

class InvalidPin(exceptions.HomeAssistantError):
    """Error to indicate the pin was incorrect"""
