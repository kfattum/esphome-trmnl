**English** | [Русский](readme.ru.md)
<table>
    <tr>
        <td><img width="480" height="360" alt="DSC00163" src="https://github.com/user-attachments/assets/c8ebdde8-9719-4faf-894d-5d4061a223ab" /></td>
        <td><img width="480" height="360" alt="Gemini_2" src="https://github.com/user-attachments/assets/e96f1e79-bff0-4bd4-8e9c-7d5a7576f1c1" /></td>
    </tr>
</table>

A repository for an ESPHome-based e-ink display project designed to display data from your [inker](https://github.com/usetrmnl/inker) ~~TRMNL BYOD~~ server and controlled by Home Assistant. The project was not created by the ESPHome or TRMNL team and is not affiliated with them.

**Documentation:** [EN](https://kfattum.github.io/en/open_projects/ESPHome-TRMNL_7+5/) | [RU](https://kfattum.github.io/open_projects/ESPHome-TRMNL_7+5/)

## Repository Contents

| Path | Description |
|---|---|
| `esphome-trmnl.yaml` | Main ESPHome firmware config. Uses `!secret` — for manual compilation. |
| `esphome-trmnl.factory.yaml` | Config used by the [web installer](https://kfattum.github.io/en/open_projects/ESPHome-TRMNL_7+5/). |
| `custom_components/esphome-trmnl/` | Custom integration for Home Assistant (`esphome_trmnl`). |
| `blueprint_controlling_epaper_display_by_presence.yaml` | Blueprint automation: pauses screen updates when no one is present. |

## How components are connected

``` mermaid
flowchart LR
    HA["Home <br> Assistant"] -- JSON API --> Inker["Inker"]
    Inker <-- HTTP requests --> ESPH["ESPHome <br> E-Ink Display"]
    HA <--> Int["Custom Integration"]
    HA --> BP["blueprint"]
    BP --> Int
    Int <-- HTTP requests --> ESPH
```

1. **ESP32 + e-paper** — runs on firmware from `esphome-trmnl.yaml` (or factory variant).
2. The device receives screen images from your **Inker** server via HTTP (`/api/display/`).
3. Registers with Inker on first boot (`/api/setup/`), then periodically requests new images.
4. **Custom integration** (`custom_components/esphome-trmnl/`) allows Home Assistant to control the display: override the image URL, change the interval, and block screen updates.
5. **Blueprint** automation that tracks presence and blocks screen updates when you are not around, so the screen doesn't update unnecessarily.
