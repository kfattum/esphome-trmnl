import datetime
import logging
from aiohttp import web
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.http import HomeAssistantView
from homeassistant.helpers.dispatcher import async_dispatcher_send

_LOGGER = logging.getLogger(__name__)

DOMAIN = "esphome_trmnl"
PLATFORMS = ["sensor", "text", "switch", "number"]

SIGNAL_NEW_DEVICE = f"{DOMAIN}_new_device"
SIGNAL_UPDATE_DEVICE = f"{DOMAIN}_update_device"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {"devices": {}})
    
    hass.http.register_view(TrmnlConfigView(hass))
    hass.http.register_view(TrmnlConfigClearView(hass))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data.pop(DOMAIN)
    return unload_ok


class TrmnlConfigView(HomeAssistantView):
    url = "/api/config/"
    name = "api:trmnl:config"
    requires_auth = False

    def __init__(self, hass):
        self.hass = hass

    async def get(self, request):
        headers = request.headers
        mac_id = headers.get("ID")

        if not mac_id:
            return web.json_response({"error": "Missing ID header"}, status=400)

        sensors_data = {
            "battery_v": headers.get("Battery-Voltage", "0"),
            "battery_prc": headers.get("Battery-Voltage-prc", "0"),
            "wifi_prc": headers.get("Wi-Fi-Signal-dB-prc", "0"),
        }

        devices = self.hass.data[DOMAIN]["devices"]
        
        if mac_id not in devices:
            _LOGGER.info(f"New TRMNL device detected: {mac_id}")
            devices[mac_id] = {
                "sensors": sensors_data,
                "override_screen_id": "",
                "override_block_update": False,
                "override_sleep_time": 0,
                "last_update": datetime.datetime.now(datetime.timezone.utc),
            }
            async_dispatcher_send(self.hass, SIGNAL_NEW_DEVICE, mac_id)
        else:
            devices[mac_id]["sensors"] = sensors_data
            devices[mac_id]["last_update"] = datetime.datetime.now(datetime.timezone.utc)
            async_dispatcher_send(self.hass, SIGNAL_UPDATE_DEVICE, mac_id)

        device_data = devices[mac_id]
        response_json = {
            "screen_design_id_override": device_data["override_screen_id"],
            "block_update": "true" if device_data["override_block_update"] else "false",
            "sleep_time": str(int(device_data["override_sleep_time"]))
        }

        return web.json_response(response_json)

class TrmnlConfigClearView(HomeAssistantView):
    url = "/api/config/clear"
    name = "api:trmnl:config_clear"
    requires_auth = False

    def __init__(self, hass):
        self.hass = hass

    async def post(self, request):
        headers = request.headers
        mac_id = headers.get("ID")

        if mac_id and mac_id in self.hass.data[DOMAIN]["devices"]:
            _LOGGER.info(f"Clearing overrides for device: {mac_id}")
            self.hass.data[DOMAIN]["devices"][mac_id]["override_screen_id"] = ""
            async_dispatcher_send(self.hass, SIGNAL_UPDATE_DEVICE, mac_id)
            return web.json_response({"status": "cleared"})

        return web.json_response({"error": "Device not found"}, status=404)
