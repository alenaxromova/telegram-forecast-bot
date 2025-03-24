from flask import Flask, render_template_string
import random
import datetime
import openai
import os

app = Flask(__name__)

# 🔐 Подключение OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")  # Временно

# 📄 Базовые тексты по числам
base_texts = {
    18: "Сегодня ты лидер. Не бойся брать инициативу на себя.",
    2: "День партнёрства и гармонии. Обрати внимание на баланс в отношениях.",
    3: "День творчества и общения. Делись радостью с другими.",
    2: "Нейтральный день. Живи спокойно и наблюдай за происходящим."
}

# 🖼 Заглушки-картинки по числам
images = {
    1: ["https://via.placeholder.com/300x200.png?text=1-A", "https://via.placeholder.com/300x200.png?text=1-B"],
    2: ["https://via.placeholder.com/300x200.png?text=2-A"],
    3: ["https://via.placeholder.com/300x200.png?text=3-A", "https://via.placeholder.com/300x200.png?text=3-B"],
    18: ["https://via.placeholder.com/300x200.png?text=Default"]
}

def calculate_number_by_date(date):
    total = sum(int(c) for c in date.strftime("%d%m%Y"))
    while total > 22:
        total = sum(int(c) for c in str(total))
    return total

@app.route("/today")
def today_forecast():
    today = datetime.date.today()
    number = calculate_number_by_date(today)

    base_text = base_texts.get(number, "Нейтральный день. Живи спокойно.")
    image_url = random.choice(images.get(number, ["https://via.placeholder.com/300x200.png?text=Default"]))

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

    html_template = f"""
    <html>
    <head><title>Прогноз на сегодня</title></head>
    <body style='font-family: Arial; padding: 20px;'>
        <h1>Прогноз на {today.strftime('%d.%m.%Y')}</h1>
        <img src="{image_url}" alt="Картинка дня"><br><br>
        <p><strong>Число дня:</strong> {number}</p>
        <p>{final_text}</p>
    </body>
    </html>
    """
    return render_template_string(html_template)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)