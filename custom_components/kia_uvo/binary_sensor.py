from . import KiaUvoEntity
from .const import DOMAIN, VEHICLE_DATA, VEHICLE_ACCOUNT

VEHICLE_DOORS = [
    ("hood", "Hood", "mdi:car"),
    ("trunk", "Trunk", "mdi:car-back"),
    ("front_left", "Front Driver", "mdi:car-door"),
    ("front_right", "Front Passenger", "mdi:car-door"),
    ("back_left", "Rear Driver", "mdi:car-door"),
    ("back_right", "Rear Passenger", "mdi:car-door")
]


async def async_setup_entry(hass, config_entry, async_add_entities):
    vehicle_data = hass.data[DOMAIN][config_entry.entry_id][VEHICLE_ACCOUNT].vehicle_data

    sensors = [
        DoorSensor(hass, config_entry, vehicle_data, door, name, icon) for door, name, icon in VEHICLE_DOORS
    ]

    async_add_entities(sensors, True)
    async_add_entities([LockSensor(hass, config_entry, vehicle_data)], True)
    async_add_entities([EngineSensor(hass, config_entry, vehicle_data)], True)
    async_add_entities([VehicleEntity(hass, config_entry, vehicle_data)], True)


class DoorSensor(KiaUvoEntity):

    def __init__(self, hass, config_entry, vehicle_data, door, name, icon):
        super().__init__(hass, config_entry, vehicle_data)
        self._door = door
        self._name = name
        self._icon = icon

    @property
    def icon(self):
        """Return the icon."""
        return "mdi:door-open" if self.is_on else "mdi:door-closed"
        return self._icon

    @property
    def is_on(self) -> bool:
        return getattr(self._vehicle_data, f'{self._door}_open')

    @property
    def state(self):
        return "on" if getattr(self._vehicle_data, f'{self._door}_open') else "off"

    @property
    def state_attributes(self):
        return {
            "last_updated": self._vehicle_data.last_updated
        }

    @property
    def device_class(self):
        """Return the device class."""
        return "door"

    @property
    def name(self):
        return f'{self._vehicle_data.vehicle["nickName"]} {self._name}'

    @property
    def unique_id(self):
        return f'kiauvo-{self._door}-{self._vehicle_data.vehicle["vehicleId"]}'



class LockSensor(KiaUvoEntity):

    def __init__(self, hass, config_entry, vehicle_data):
        super().__init__(hass, config_entry, vehicle_data)

    @property
    def icon(self):
        """Return the icon."""
        return "mdi:lock" if self.is_on else "mdi:lock-open-variant"

    @property
    def is_on(self) -> bool:
        return self._vehicle_data.door_lock

    @property
    def state(self):
        return "off" if self._vehicle_data.door_lock else "on"

    @property
    def state_attributes(self):
        return {
            "last_updated": self._vehicle_data.last_updated
        }

    @property
    def device_class(self):
        """Return the device class."""
        return "lock"

    @property
    def name(self):
        return f'{self._vehicle_data.vehicle["nickName"]} Door Lock'

    @property
    def unique_id(self):
        return f'kiauvo-door-lock-{self._vehicle_data.vehicle["vehicleId"]}'



class EngineSensor(KiaUvoEntity):

    def __init__(self, hass, config_entry, vehicle_data):
        super().__init__(hass, config_entry, vehicle_data)

    @property
    def icon(self):
        """Return the icon."""
        return "mdi:engine" if self.is_on else "mdi:engine-off"

    @property
    def is_on(self) -> bool:
        return self._vehicle_data.engine

    @property
    def state(self):
        return "on" if self._vehicle_data.engine else "off"

    @property
    def state_attributes(self):
        return {
            "last_updated": self._vehicle_data.last_updated,
            "presets": self._vehicle_data.engine_start_presets
        }

    @property
    def device_class(self):
        """Return the device class."""
        return "power"

    @property
    def name(self):
        return f'{self._vehicle_data.vehicle["nickName"]} Engine'

    @property
    def unique_id(self):
        return f'kiauvo-engine-{self._vehicle_data.vehicle["vehicleId"]}'



class VehicleEntity(KiaUvoEntity):
    def __init__(self, hass, config_entry, vehicle_data):
        super().__init__(hass, config_entry, vehicle_data)

    @property
    def state(self):
        return "on"

    @property
    def is_on(self) -> bool:
        return True

    @property
    def state_attributes(self):
        return {
            "vehicle": self._vehicle_data.vehicle,
            "status": self._vehicle_data.status,
            "maintenance": self._vehicle_data.maintenance
        }

    @property
    def name(self):
        return f'{self._vehicle_data.vehicle["nickName"]} Data'

    @property
    def unique_id(self):
        return f'kiauvo-all-data-{self._vehicle_data.vehicle["vehicleId"]}'


