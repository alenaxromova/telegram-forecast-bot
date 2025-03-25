from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI
import os
import random
import datetime
import pytz
import requests

app = Flask(__name__)

# 🔐 Подключение OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# ✨ Базовые тексты по числам (можно заменить своими)
base_texts = {
    1: "Сегодня ты лидер. Не бойся брать инициативу на себя.",
    2: "День партнёрства и гармонии. Обрати внимание на баланс в отношениях.",
    3: "День творчества и общения. Делись радостью с другими.",
    # ... добавь все 22 текста по числам
}

# 🖼 Заглушки-картинки по числам
images = {
    1: [
        "https://via.placeholder.com/300x200.png?text=1A",
        "https://via.placeholder.com/300x200.png?text=1B"
    ],
    2: [
        "https://via.placeholder.com/300x200.png?text=2A",
        "https://via.placeholder.com/300x200.png?text=2B"
    ],
    # ... добавить больше при необходимости
}

def calculate_number_by_date(date):
    total = sum(int(c) for c in date.strftime("%d%m%Y"))
    while total > 22:
        total = sum(int(c) for c in str(total))
    return total

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/auth.html')
def auth_html():
    return send_from_directory('.', 'auth.html')

@app.route('/today')
def today_forecast():
    tz = request.args.get('tz', 'UTC')
    try:
        user_tz = pytz.timezone(tz)
    except:
        user_tz = pytz.UTC

    now = datetime.datetime.now(user_tz)
    date_str = now.strftime("%Y-%m-%d")
    number = calculate_number_by_date(now)

    base_text = base_texts.get(number, "Нейтральный день. Живи спокойно.")
    image_url = random.choice(images.get(number, ["https://via.placeholder.com/300x200.png?text=Default"]))

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты магический помощник. Расширь и укрась этот текст, не добавляя новых смыслов."},
                {"role": "user", "content": base_text}
            ]
        )
        final_text = response.choices[0].message.content.strip()
    except Exception as e:
        final_text = f"[Ошибка OpenAI] {str(e)}"

    return jsonify({
        "date": date_str,
        "number": number,
        "image": image_url,
        "text": final_text
    })

# === 📩 Telegram Webhook ===
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    data = request.get_json()

    if 'message' in data and data['message'].get('text') == '/start':
        chat_id = data['message']['chat']['id']
        send_button(chat_id)

    return jsonify(ok=True)

def send_button(chat_id):
    webapp_url = "https://telegram-forecast-bot.onrender.com/"
    message = "✨ Нажми на кнопку ниже, чтобы получить прогноз на сегодня:"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "reply_markup": {
            "inline_keyboard": [[
                {
                    "text": "🔮 Получить прогноз",
                    "web_app": {
                        "url": webapp_url
                    }
                }
            ]]
        }
    }
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        json=payload
    )

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

