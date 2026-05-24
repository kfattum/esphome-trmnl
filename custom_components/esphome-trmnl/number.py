from homeassistant.components.number import NumberEntity
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from .__init__ import DOMAIN, SIGNAL_NEW_DEVICE

async def async_setup_entry(hass, config_entry, async_add_entities):
    async def add_new_device(mac_id):
        async_add_entities([TrmnlSleepTimeNumber(hass, mac_id)])
    async_dispatcher_connect(hass, SIGNAL_NEW_DEVICE, add_new_device)

    for mac_id in hass.data[DOMAIN]["devices"]:
        await add_new_device(mac_id)

class TrmnlSleepTimeNumber(NumberEntity):
    def __init__(self, hass, mac_id):
        self.hass = hass
        self._mac_id = mac_id
        self._attr_name = f"TRMNL Sleep Time ({mac_id})"
        self._attr_unique_id = f"{mac_id}_sleep_time"
        self._attr_native_min_value = 0
        self._attr_native_max_value = 9999999
        self._attr_native_step = 60
        self._attr_native_unit_of_measurement = "s"
        self._attr_icon = "mdi:timer-outline"

    @property
    def native_value(self):
        return self.hass.data[DOMAIN]["devices"][self._mac_id]["override_sleep_time"]

    async def async_set_native_value(self, value: float) -> None:
        self.hass.data[DOMAIN]["devices"][self._mac_id]["override_sleep_time"] = int(value)
        self.async_write_ha_state()

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._mac_id)}}
