from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import logging
import os
import threading
from flask import Flask

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Получаем токен
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")

# --- КНОПКИ ---
keyboard = [
    ["Показать меню"],
    ["Дополнительные услуги"],
    ["Режим работы"],
    ["Связаться с администратором"]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# --- ОБРАБОТЧИКИ ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я — бот доставки отеля «Царская охота» на Алтае 🌲👋\n"
        "Горный воздух, тишина леса… А еду мы принесём сами — тёплую, домашнюю и прямо к тебе.\n"
        "\nВыбери, что хочешь узнать:",
        reply_markup=reply_markup
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Показать меню":
        try:
            with open("menu.pdf", "rb") as pdf_file:
                caption = (
                    "📄 Вот наше меню — выбирайте, что душе угодно! 🍽️\n\n"
                    "📞 <b>Как сделать заказ:</b>\n"
                    "Позвоните нам по номеру телефона:\n"
                    "<a href='tel:+79833292301'>+7 (983) 329-23-01</a>\n\n"
                    "🚚 <i>Доставка прямо к номеру или в беседку!</i>"
                )
                await update.message.reply_document(
                    document=pdf_file,
                    caption=caption,
                    parse_mode="HTML"
                )
        except FileNotFoundError:
            await update.message.reply_text("❗ Ошибка: файл menu.pdf не найден.")
        except Exception as e:
            await update.message.reply_text(f"❗ Ошибка: {e}")

    elif text == "Дополнительные услуги":
        try:
            with open("dop.jpeg", "rb") as jpeg_file:
                await update.message.reply_photo(
                    photo=jpeg_file,
                    caption="📦 <b>Дополнительные услуги:</b>\n\n"
                            "• Гриль-наборы: свинина, птица, рыба, овощи 🥩\n"
                            "• Уголь, розжиг, подготовка костровища 🔥\n"
                            "• Баня с купелью 💦\n"
                            "• Услуги стирки и глажки 🧺\n\n"
                            "Закажите всё к себе в номер!\n"
                            "📞 Звоните: <a href='tel:+79139900025'>+7 (913) 990-00-25</a>\n\n"
                            "Всё для комфортного отдыха в горах! 🌿",
                    parse_mode="HTML"
                )
        except FileNotFoundError:
            await update.message.reply_text("❗ Ошибка: файл dop.jpeg не найден.")
        except Exception as e:
            await update.message.reply_text(f"❗ Ошибка: {e}")

    elif text == "Режим работы":
        try:
            await update.message.reply_text(
                "🕰️ <b>Режим работы кухни:</b>\n"
                "Ежедневно с <b>9:00 до 21:00</b>\n\n"
                "🍽️ <b>Что можно заказать:</b>\n"
                "• Завтрак в постель 🍳\n"
                "• Обед в домик 🍲\n"
                "• Домашний ужин на террасу 🥗🥖\n"
                "• Кофе с видом на природу ☕\n"
                "• И всё, что душе угодно! 🌿\n\n"
                "📞 <b>Как сделать заказ:</b>\n"
                "Позвоните нам по номеру телефона:\n"
                '<a href="tel:+79833292301">+7 (983) 329-23-01</a>\n\n'
                "🚚 Доставка прямо к номеру или в беседку!",
                parse_mode="HTML"
            )
        except Exception as e:
            await update.message.reply_text(f"❗ Ошибка: {e}")

    elif text == "Связаться с администратором":
        await update.message.reply_text(
            "📞 Напишите администратору: @tsarskaya_ohota_altay\n"
            "Или звоните: +7 (913) 990-00-25"
        )

    else:
        await update.message.reply_text(
            "Пожалуйста, используйте кнопки ниже.",
            reply_markup=reply_markup
        )

# --- ВЕБ-СЕРВЕР ДЛЯ RENDER ---
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Бот работает! Это техническая страница для Render."

def run_server():
    port = int(os.getenv('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# --- ЗАПУСК БОТА ---
def main():
    # Запускаем веб-сервер в отдельном потоке
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Создаём приложение бота
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    # Запускаем polling
    print("✅ Бот запущен и слушает обновления...")
    application.run_polling()

# Запуск
if __name__ == "__main__":
    main()