from flask import Flask, jsonify
from datetime import datetime
import openai
import os
import random

app = Flask(__name__)

# API-ключ из переменных окружения (безопасно)
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Базовые тексты по числам (как подсказки для GPT)
base_texts = {
    1: "Сегодня ты лидер. Не бойся брать инициативу на себя.",
    2: "День партнёрства и гармонии. Обрати внимание на баланс в отношениях.",
    3: "День творчества и общения. Делись радостью с другими.",
}

# Заглушки-картинки
images = {
    1: ["https://via.placeholder.com/300x200.png?text=1A", "https://via.placeholder.com/300x200.png?text=1B"],
    2: ["https://via.placeholder.com/300x200.png?text=2A", "https://via.placeholder.com/300x200.png?text=2B"],
    3: ["https://via.placeholder.com/300x200.png?text=3A"],
}

# Расчёт числа по дате
def calculate_number_by_date(date):
    total = sum(int(c) for c in date.strftime("%d%m%Y"))
    while total > 22:
        total = sum(int(c) for c in str(total))
    return total if total in base_texts else 1

@app.route("/today")
def today_forecast():
    today = datetime.today()
    number = calculate_number_by_date(today)
    base_text = base_texts.get(number, "Нейтральный день.")

    image_url = random.choice(images.get(number, ["https://via.placeholder.com/300x200.png?text=Default"]))

    # GPT-запрос
    try:
        response = openai.ChatCompletion.create(
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
        "date": today.strftime("%Y-%m-%d"),
        "number": number,
        "text": final_text,
        "image": image_url
    })

# Запуск для Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
