import requests
import os

# Получаем токен из секретов Replit
BOT_TOKEN = os.getenv("BOT_TOKEN")
URL = f"https://api.telegram.org/bot{BOT_TOKEN}/setChatMenuButton"

# Настраиваем кнопку меню с мини-приложением
payload = {
    "menu_button": {
        "type": "web_app",
        "text": "🔮 Прогноз на день",
        "web_app": {
            "url": "https://forecast-test-olenaxromova.replit.app/today"
        }
    }
}

response = requests.post(URL, json=payload)

print("Статус:", response.status_code)
print("Ответ:", response.text)