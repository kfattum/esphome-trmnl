[English](readme.md) | **Русский**
<table>
    <tr>
        <td><img width="1440" height="1080" alt="DSC00163" src="https://github.com/user-attachments/assets/c8ebdde8-9719-4faf-894d-5d4061a223ab" /></td>
        <td><img width="1438" height="1080" alt="Gemini_2" src="https://github.com/user-attachments/assets/e96f1e79-bff0-4bd4-8e9c-7d5a7576f1c1" /></td>
    </tr>
</table>

Репозиторий проекта E-ink дисплея на ESPHome, предназначенного для отображения данных с вашего сервера [inker](https://github.com/usetrmnl/inker) ~~TRMNL BYOD~~ и управляемый Home Assistant. Проект не создан командой ESPHome или ТRMNL и не аффилирован с ними.

**Документация:** [EN](https://3dpm.ru/en/open_projects/ESPHome-TRMNL_7+5/) | [RU](https://3dpm.ru/open_projects/ESPHome-TRMNL_7+5/)
``` mermaid
flowchart LR
    HA["Home <br> Assistant"] -- JSON API --> Inker["Inker"]
    Inker <-- HTTP-запросы --> ESPH["ESPHome <br> E-Ink дисплей"]
    HA <--> Int["Кастомная интеграция"]
    HA --> BP["blueprint"]
    BP --> Int
    Int <-- HTTP-запросы --> ESPH
```

 


