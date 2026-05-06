<table>
    <tr>
        <td><img width="1440" height="1080" alt="DSC00163" src="https://github.com/user-attachments/assets/c8ebdde8-9719-4faf-894d-5d4061a223ab" /></td>
        <td><img width="1438" height="1080" alt="Gemini_2" src="https://github.com/user-attachments/assets/e96f1e79-bff0-4bd4-8e9c-7d5a7576f1c1" /></td>
    </tr>
</table>

A repository for an ESPHome-based e-ink display project designed to display data from your [inker](https://github.com/usetrmnl/inker) ~~TRMNL BYOD~~ server and controlled by Home Assistant.

**Documentation:** [EN](https://3dpm.ru/en/open_projects/ESPHome-TRMNL_7+5/)

---
Репозиторий проекта E-ink дисплея на ESPHome, предназначенного для отображения данных с вашего сервера [inker](https://github.com/usetrmnl/inker) ~~TRMNL BYOD~~ и управляемый Home Assistant.

**Документация:** [RU](https://3dpm.ru/open_projects/ESPHome-TRMNL_7+5/)

``` mermaid
flowchart LR
    HA["Home <br> Assistant"] -- JSON API --> Inker["Inker"]
    RSS["RSS-каналы"] --> Inker
    Inker -- PNG --> ESPH["ESPHome <br> E-Ink дисплей"]
    HA <--> MQTT_Int["интеграция <br> MQTT"]
    HA --> BP["blueprint"]
    BP --> MQTT_Int
    MQTT_Int <--> Mosq["Mosquitto <br> broker"]
    Mosq <-- MQTT --> ESPH
```

