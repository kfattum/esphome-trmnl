from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from .__init__ import DOMAIN, SIGNAL_NEW_DEVICE

async def async_setup_entry(hass, config_entry, async_add_entities):
    async def add_new_device(mac_id):
        async_add_entities([TrmnlBlockUpdateSwitch(hass, mac_id)])
    async_dispatcher_connect(hass, SIGNAL_NEW_DEVICE, add_new_device)

    for mac_id in hass.data[DOMAIN]["devices"]:
        await add_new_device(mac_id)

class TrmnlBlockUpdateSwitch(SwitchEntity):
    def __init__(self, hass, mac_id):
        self.hass = hass
        self._mac_id = mac_id
        self._attr_name = f"TRMNL Block Update ({mac_id})"
        self._attr_unique_id = f"{mac_id}_block_update"
        self._attr_icon = "mdi:cancel"

    @property
    def is_on(self):
        return self.hass.data[DOMAIN]["devices"][self._mac_id]["override_block_update"]

    async def async_turn_on(self, **kwargs):
        self.hass.data[DOMAIN]["devices"][self._mac_id]["override_block_update"] = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self.hass.data[DOMAIN]["devices"][self._mac_id]["override_block_update"] = False
        self.async_write_ha_state()

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._mac_id)}}
