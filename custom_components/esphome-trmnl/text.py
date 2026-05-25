from homeassistant.components.text import TextEntity
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from .__init__ import DOMAIN, SIGNAL_NEW_DEVICE, SIGNAL_UPDATE_DEVICE

async def async_setup_entry(hass, config_entry, async_add_entities):
    async def add_new_device(mac_id):
        async_add_entities([TrmnlOverrideText(hass, mac_id)])
    async_dispatcher_connect(hass, SIGNAL_NEW_DEVICE, add_new_device)

    for mac_id in hass.data[DOMAIN]["devices"]:
        await add_new_device(mac_id)

class TrmnlOverrideText(TextEntity):
    def __init__(self, hass, mac_id):
        self.hass = hass
        self._mac_id = mac_id
        self._attr_name = "Override URL"
        self._attr_unique_id = f"{mac_id}_override_screen_id"

    @property
    def native_value(self):
        return self.hass.data[DOMAIN]["devices"][self._mac_id]["override_screen_id"]

    async def async_set_value(self, value: str) -> None:
        self.hass.data[DOMAIN]["devices"][self._mac_id]["override_screen_id"] = value
        self.async_write_ha_state()

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._mac_id)}}

    async def async_added_to_hass(self):
        self.async_on_remove(
            async_dispatcher_connect(self.hass, SIGNAL_UPDATE_DEVICE, self._update_callback)
        )

    def _update_callback(self, mac_id):
        if mac_id == self._mac_id:
            self.async_write_ha_state()
