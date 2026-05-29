import datetime

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import EntityCategory
from .__init__ import DOMAIN, SIGNAL_NEW_DEVICE, SIGNAL_UPDATE_DEVICE

async def async_setup_entry(hass, config_entry, async_add_entities):
    async def add_new_device(mac_id):
        entities = [
            TrmnlSensor(hass, mac_id, "battery_v", "Battery Voltage", "V", SensorDeviceClass.VOLTAGE, precision=2),
            TrmnlSensor(hass, mac_id, "battery_prc", "Battery", "%", SensorDeviceClass.BATTERY, precision=0),
            TrmnlSensor(hass, mac_id, "wifi_prc", "Wi-Fi Signal", "%", None, precision=0),
            TrmnlLastUpdateSensor(hass, mac_id),
        ]
        async_add_entities(entities)

    async_dispatcher_connect(hass, SIGNAL_NEW_DEVICE, add_new_device)

    for mac_id in hass.data[DOMAIN]["devices"]:
        await add_new_device(mac_id)

class TrmnlSensor(SensorEntity):
    def __init__(self, hass, mac_id, sensor_key, name, unit, device_class, precision=2):
        self.hass = hass
        self._mac_id = mac_id
        self._sensor_key = sensor_key
        self._precision = precision
        self._attr_has_entity_name = True
        self._attr_translation_key = sensor_key
        self._attr_unique_id = f"{mac_id}_{sensor_key}"
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        raw = self.hass.data[DOMAIN]["devices"][self._mac_id]["sensors"].get(self._sensor_key)
        try:
            return round(float(raw), self._precision)
        except (ValueError, TypeError):
            return raw

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._mac_id)},
            "name": "ESPHome-TRMNL Display",
            "connections": {("mac", self._mac_id)}
        }

    async def async_added_to_hass(self):
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass, SIGNAL_UPDATE_DEVICE, self._update_callback
            )
        )

    def _update_callback(self, mac_id):
        if mac_id == self._mac_id:
            self.async_write_ha_state()


class TrmnlLastUpdateSensor(SensorEntity):
    def __init__(self, hass, mac_id):
        self.hass = hass
        self._mac_id = mac_id
        self._attr_has_entity_name = True
        self._attr_translation_key = "last_update"
        self._attr_unique_id = f"{mac_id}_last_update"
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self):
        return self.hass.data[DOMAIN]["devices"][self._mac_id].get("last_update")

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._mac_id)},
            "name": "ESPHome-TRMNL Display",
        }

    async def async_added_to_hass(self):
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass, SIGNAL_UPDATE_DEVICE, self._update_callback
            )
        )

    def _update_callback(self, mac_id):
        if mac_id == self._mac_id:
            self.async_write_ha_state()
