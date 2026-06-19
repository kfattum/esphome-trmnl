**English** | [Русский](readme.ru.md)

![img](/img/logo2x.png)

The custom `esphome_trmnl` integration provides two-way communication between Home Assistant and an E-Ink display running on ESPHome. It allows you to:

* Receive telemetry from the display (battery voltage, battery level, Wi-Fi signal strength).


* Block screen refreshes.


* Change the refresh interval.


* Override the image URL to display arbitrary content.



## Supported Devices

Displays running the ESPHome-TRMNL firmware v2.0.0+.

## Installation

=== "Using HACS (recommended)"
    This method allows you to receive updates directly on the HACS main page. If HACS isn't already installed, download it by following the instructions on the [hacs.xyz/docs/setup/download/](https://hacs.xyz/docs/use/download/prerequisites/) page.

    * In HACS, go to the menu in the upper right corner, then select "Custom Repositories."
    * Then add the repository https://github.com/kfattum/esphome-trmnl and select "Integration." After that, click "Add."
    * After adding, click the "Cancel" button next to the "Add" button.
    * Download the integration by clicking [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=kfattum&repository=esphome-trmnl&category=Integrations){.ha-badge target=_blank} or search for ESPHome-TRMNL.
    * Restart Home Assistant for the system to recognize the new files.
    * Add the integration to HA by clicking [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=esphome_trmnl){.ha-badge target=_blank} or go to Settings -> Devices & Services -> Add Integration, search for "ESPHome-TRMNL" -> Add
    * When you turn on the screen, it should automatically appear in the **"ESPHome-TRMNL"** integration.

=== "Without "HACS""
    This method requires manually copying files and monitoring updates yourself.

    2. Download the archive [esphome_trmnl_custom_integration.zip](https://github.com/kfattum/esphome-trmnl/releases/latest/download/esphome_trmnl_custom_integration.zip){target=_blank}
    3. Unzip the downloaded archive on your computer.
    4. Find the "custom_components/esphome_trmnl" folder inside and copy the "esphome_trmnl" folder to the "custom_components" directory of your Home Assistant configuration.
    5. Restart Home Assistant for the system to recognize the new files.
    6. Go to Settings -> Devices & Services -> Add Integration, search for "ESPHome-TRMNL" -> Add
    6. When you turn on your screen, it should automatically appear in the "ESPHome-TRMNL" integration.

## Integration Entities

Each display creates a set of entities.

### Sensors

| Entity | Description |
| --- | --- |
| `sensor` Battery Voltage | Battery voltage (V) |
| `sensor` Battery Level | Charge level (%) |
| `sensor` Wi-Fi Signal | Wi-Fi signal strength (%) |
| `sensor` Last Update | Time of the last response from the display |

### Controls

| Type | Name | Description |
| --- | --- | --- |
| `switch` | Block display refresh | Blocks screen refresh (ON — screen does not refresh) |
| `number` | Sleep Time | Interval between refreshes in seconds (0 = interval from inker, step 60, max 9,999,999) |
| `text` | Image URL | http link to a PNG image with an 800x480 resolution to show on the screen (for example, [http://192.168.1.100:8124/api/device-images/design/2](https://www.google.com/url?sa=E&source=gmail&q=http://192.168.1.100:8124/api/device-images/design/2) will display the 2nd inker screen). If the field is empty — the display shows content from Inker. |

> Note: Entities on the ESP side (Inker Server URL, HA Server URL, Language) are managed through the ESP32 web interface. They are not part of this integration.
> 
> 

### Resetting Control Entity Values

Press and hold the button on the case for more than 5 seconds in deep sleep mode — this will reset `Image URL`, `Sleep Time`, and `Block display refresh` to their default values.

## Automation Example

This example demonstrates how to dynamically manage the E-Ink display throughout the day: switching the displayed content in the evening and putting the device into deep power-saving mode at night.

### Automation Scenario

1. **Evening (20:00):** A command to change the image (inker screen) is sent to the display via the `text` entity. An evening template is shown on the screen (e.g., a cozy dashboard or a clock).

2. **Midnight (00:00):** The display is switched to **night mode** to save battery:



* The refresh interval (`number`) is increased to `17800` seconds (~5 hours).


* The refresh block mode (`switch`) is turned on, putting the device to sleep.


* The URL is cleared. Now, when the screen wakes up, the inker playlist will be displayed.



3. **Morning (05:30):** The display **wakes up**:



* Sleep time is reset to `0` (returning to the standard polling interval).


* The refresh block is turned off, and the display updates the data on the screen again.



??? example "Automation Code (YAML)"

    You can copy this code into the text mode of the Home Assistant automation editor:

    ```yaml

    alias: "ESPHome-TRMNL: Screen management throughout the day"
    description: "Automatic screen switching and deep sleep at night"
    triggers:

    * trigger: time
    at: "20:00:00"
    id: evening
    * trigger: time
    at: "00:00:00"
    id: midnight
    * trigger: time
    at: "05:30:00"
    id: morning
    conditions: []
    actions:
    * choose:
    # EVENING MODE


    * conditions:
    * condition: trigger
    id:
    * evening
    sequence:


    * action: text.set_value
    target:
    device_id: ad5052c25da850ff28860ef907f3367e
    data:
    value: http://192.168.1.100:8124/api/device-images/design/2
    note: "Setting the evening screen layout"




    # NIGHT MODE (POWER SAVING)


    * conditions:
    * condition: trigger
    id:
    * midnight
    sequence:


    * action: number.set_value
    target:
    area_id: prikhozhaia
    data:
    value: "17800"
    note: "Increasing the sleep interval until morning"
    * action: switch.turn_on
    target:
    area_id: prikhozhaia
    note: "Turning on refresh block (deep sleep)"
    * action: text.set_value
    target:
    device_id: ad5052c25da850ff28860ef907f3367e
    data: {}
    note: "Resetting custom URL"




    # MORNING WAKE UP


    * conditions:
    * condition: trigger
    id:
    * morning
    sequence:


    * action: number.set_value
    target:
    area_id: prikhozhaia
    data:
    value: "0"
    note: "Resetting sleep interval to standard"
    * action: switch.turn_off
    target:
    area_id: prikhozhaia
    note: "Disabling the block, starting refreshes"
    mode: single





    ```

## Troubleshooting

### Display does not appear in the integration

1. Ensure that the display is turned on and connected to the correct Wi-Fi network.
2. Check that the display has access to Home Assistant (HA URL is configured in the ESP web interface).

    !!! info "Changing HA and Inker URL addresses" 
        The standard "HA" ([http://homeassistant.local:8123](http://homeassistant.local:8123)) and "Inker" ([http://homeassistant.local:8124](http://homeassistant.local:8124)) URL addresses can be changed in the ESP32 web interface (the default login and password for the web interface is "esphome-trmnl"). Press the button to wake up the board, wait a second, then press and hold the button for 5 seconds to enter the settings mode. If the board is connected to Wi-Fi, a QR code with a link to the web interface will be displayed; if it is not connected, a QR code with a link to the [captive portal](https://esphome.io/components/captive_portal/){target=_blank} will be displayed.

* Check the display logs via [web.esphome.io](https://web.esphome.io/) (connect the ESP via USB).

### The word ERROR is on the screen

* The display cannot connect to Wi-Fi or Inker.
* Make sure you are not using https.
* Check the display logs via [web.esphome.io](https://web.esphome.io/) (connect the ESP via USB).