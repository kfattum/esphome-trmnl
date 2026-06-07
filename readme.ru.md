[English](readme.md) | **Русский**
<table>
    <tr>
        <td><img width="480" height="360" alt="DSC00163" src="https://github.com/user-attachments/assets/c8ebdde8-9719-4faf-894d-5d4061a223ab" /></td>
        <td><img width="480" height="360" alt="Gemini_2" src="https://github.com/user-attachments/assets/e96f1e79-bff0-4bd4-8e9c-7d5a7576f1c1" /></td>
    </tr>
</table>

Репозиторий проекта E-ink дисплея на ESPHome, предназначенного для отображения данных с вашего сервера [inker](https://github.com/usetrmnl/inker) ~~TRMNL BYOD~~ и управляемый Home Assistant. Проект не создан командой ESPHome или ТRMNL и не аффилирован с ними.

## **Документация:** [EN](https://kfattum.github.io/en/open_projects/ESPHome-TRMNL_7+5/) | [RU](https://kfattum.github.io/open_projects/ESPHome-TRMNL_7+5/)


## Содержимое репозитория

| Путь | Описание |
|---|---|
| `esphome-trmnl.yaml` | Основной конфиг прошивки ESPHome. Использует `!secret` — для ручной компиляции. |
| `esphome-trmnl.factory.yaml` | Конфиг который используется [web installer](https://kfattum.github.io/en/open_projects/ESPHome-TRMNL_7+5/). |
| `custom_components/esphome-trmnl/` | Кастомная интеграция для Home Assistant (`esphome_trmnl`). |
| `blueprint_controlling_epaper_display_by_presence.yaml` | Blueprint-автоматизация: приостанавливает обновление экрана при отсутствии людей. |

## Как компоненты связаны

``` mermaid
flowchart LR
    HA["Home <br> Assistant"] -- JSON API --> Inker["Inker"]
    Inker <-- HTTP-запросы --> ESPH["ESPHome <br> E-Ink дисплей"]
    HA <--> Int["Кастомная интеграция"]
    HA --> BP["blueprint"]
    BP --> Int
    Int <-- HTTP-запросы --> ESPH
```

1. **ESP32 + e-paper** — работает на прошивке из `esphome-trmnl.yaml` (или factory-варианта).
2. Устройство получает изображения экрана с вашего **Inker**-сервера по HTTP (`/api/display/`).
3. При первой загрузке регистрируется в Inker (`/api/setup/`), затем периодически запрашивает новые изображения.
4. **Кастомная интеграция** (`custom_components/esphome-trmnl/`) позволяет Home Assistant управлять дисплеем: переопределять URL изображения, изменять интервал и блокировать обновление экрана.
5. **Blueprint** автоматизация которая отслеживает присутствие и блокирует обновления экрана когда вас нет рядом, чтобы экран не обновлялся попусту.
