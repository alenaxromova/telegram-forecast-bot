from flask import Flask, jsonify, request
from datetime import datetime
from openai import OpenAI
import os
import random
import pytz

app = Flask(__name__)

# 🔐 OpenAI клиент
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Базовые тексты по числам (добавь свои позже)
base_texts = {
    1: "Ты — лидер. Действуй смело.",
    2: "Слушай и будь внимательным.",
    3: "Пусть сегодня будет ярким!",
    4: "Сохраняй устойчивость — ты как скала.",
    5: "День перемен. Откройся новому.",
    6: "Позаботься о близких. И о себе.",
    7: "Отличный день для учёбы и уединения.",
    8: "Финансовый день. Будь честен и точен.",
    9: "Пора подвести итоги. Идёт завершение цикла.",
}

# Картинки по числам (пока заглушки)
images = {
    1: ["https://via.placeholder.com/300x200.png?text=1A", "https://via.placeholder.com/300x200.png?text=1B"],
    2: ["https://via.placeholder.com/300x200.png?text=2A"],
    3: ["https://via.placeholder.com/300x200.png?text=3A"],
    4: ["https://via.placeholder.com/300x200.png?text=4A"],
    5: ["https://via.placeholder.com/300x200.png?text=5A"],
    6: ["https://via.placeholder.com/300x200.png?text=6A"],
    7: ["https://via.placeholder.com/300x200.png?text=7A"],
    8: ["https://via.placeholder.com/300x200.png?text=8A"],
    9: ["https://via.placeholder.com/300x200.png?text=9A"],
}

# 🔢 Расчёт числа из даты
def calculate_number_by_date(date):
    total = sum(int(c) for c in date.strftime("%d%m%Y"))
    while total > 22:
        total = sum(int(c) for c in str(total))
    return total if total in base_texts else 1

@app.route("/today")
def today_forecast():
    # Получаем часовой пояс из запроса
    tz_name = request.args.get("tz", "UTC")
    try:
        user_tz = pytz.timezone(tz_name)
    except Exception:
        user_tz = pytz.UTC

    now = datetime.now(user_tz)
    number = calculate_number_by_date(now)
    base_text = base_texts.get(number, "Нейтральный день.")
    image_url = random.choice(images.get(number, ["https://via.placeholder.com/300x200.png?text=Default"]))

    # Запрос к OpenAI
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
        "date": now.strftime("%Y-%m-%d"),
        "number": number,
        "text": final_text,
        "image": image_url
    })

# 🟢 Запуск для Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
