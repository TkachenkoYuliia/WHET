# -*- coding: utf-8 -*-
"""
Telegram бот WeT - меню на день з продуктів у холодильнику.
"""
import os
from dotenv import load_dotenv
import telebot
from telebot import types

from parser import parse_products
from recipes import get_recipes_by_ingredients, generate_menu_variants, RECIPES, normalize_ingredient

load_dotenv()
BOT_TOKEN = os.getenv("TG_BOT_KEY")
if not BOT_TOKEN:
    raise ValueError("Встановіть TG_BOT_KEY у файлі .env")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# Стан користувачів: chat_id -> {...}
user_state = {}


def get_state(chat_id):
    if chat_id not in user_state:
        user_state[chat_id] = {"step": None, "products": {}, "variants": [], "chosen": None}
    return user_state[chat_id]


def main_menu_keyboard():
    """Головне меню."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📋 Додати продукти")
    btn2 = types.KeyboardButton("🍽 Згенерувати меню")
    btn3 = types.KeyboardButton("ℹ️ Допомога")
    markup.add(btn1, btn2)
    markup.add(btn3)
    return markup


@bot.message_handler(commands=["start"])
def cmd_start(message):
    s = get_state(message.chat.id)
    s["step"] = "idle"
    s["products"] = {}
    s["variants"] = []
    s["chosen"] = None
    bot.send_message(
        message.chat.id,
        f"Привіт, <b>{message.from_user.first_name}</b>! 👋\n\n"
        "Я бот <b>WeT</b> — допоможу скласти збалансоване меню на день з продуктів у твоєму холодильнику.\n\n"
        "Використовуй меню нижче або напиши список продуктів із кількістю.\n"
        "Наприклад:\n"
        "<code>яйця 3 шт, молоко 200 г, борошно 300 г, помідори 2 шт</code>",
        reply_markup=main_menu_keyboard(),
    )


@bot.message_handler(commands=["help"])
def cmd_help(message):
    bot.send_message(
        message.chat.id,
        "ℹ️ <b>Допомога</b>\n\n"
        "1️⃣ Напиши список продуктів і кількість у форматі:\n"
        "   • <code>продукт кількість шт</code> — для штук\n"
        "   • <code>продукт кількість г</code> — для грамів\n\n"
        "2️⃣ Натисни «Згенерувати меню» — отримаєш 3 варіанти меню на день.\n\n"
        "3️⃣ Обери варіант — побачиш список страв.\n\n"
        "4️⃣ Натисни на страву — отримаєш повний рецепт.\n\n"
        "Приклад:\n<code>яйця 5 шт, молоко 500 г, борошно 300 г, сир 200 г</code>",
        reply_markup=main_menu_keyboard(),
    )


@bot.message_handler(func=lambda m: m.text == "ℹ️ Допомога")
def btn_help(message):
    cmd_help(message)


@bot.message_handler(func=lambda m: m.text == "📋 Додати продукти")
def btn_add_products(message):
    s = get_state(message.chat.id)
    s["step"] = "waiting_products"
    products_text = ""
    if s["products"]:
        products_text = "\n\nПоточний список:\n" + ", ".join(
            f"{k} {v[0]} {v[1]}" for k, v in s["products"].items()
        )
    bot.send_message(
        message.chat.id,
        "📋 Напиши список продуктів з кількістю.\n\n"
        "Формат: <code>продукт кількість шт/г</code>\n"
        "Через кому або з нового рядка.\n\n"
        "Приклад:\n"
        "<code>яйця 3 шт, молоко 200 г, борошно 300 г</code>" + products_text,
    )


@bot.message_handler(func=lambda m: m.text == "🍽 Згенерувати меню")
def btn_generate(message):
    s = get_state(message.chat.id)
    if not s["products"]:
        bot.send_message(
            message.chat.id,
            "Спочатку додай продукти — натисни «Додати продукти» або напиши список.",
            reply_markup=main_menu_keyboard(),
        )
        return

    recipes = get_recipes_by_ingredients(s["products"])
    if not recipes:
        bot.send_message(
            message.chat.id,
            "😔 На жаль, за твоїми продуктами не знайдено підходящих страв. "
            "Спробуй додати більше продуктів: яйця, молоко, борошно, овочі, м'ясо, сир тощо.",
            reply_markup=main_menu_keyboard(),
        )
        return

    variants = generate_menu_variants(recipes, 3)
    s["variants"] = variants
    s["step"] = "choose_menu"

    msg = (
        "🍽 Ось 3 варіанти збалансованого меню на день:\n\n"
        "Оберіть варіант кнопками нижче 👇"
    )
    markup = types.InlineKeyboardMarkup()
    for i, v in enumerate(variants, 1):
        b, l, d = v[0], v[1], v[2]
        label = f"Варіант {i}: {b['name']} / {l['name']} / {d['name']}"
        markup.add(types.InlineKeyboardButton(label, callback_data=f"menu_{i}"))
    bot.send_message(message.chat.id, msg, reply_markup=markup)


@bot.callback_query_handler(func=lambda c: c.data.startswith("menu_"))
def callback_choose_menu(callback):
    idx = int(callback.data.split("_")[1])
    s = get_state(callback.message.chat.id)
    if not s["variants"] or idx < 1 or idx > len(s["variants"]):
        bot.answer_callback_query(callback.id)
        return

    chosen = s["variants"][idx - 1]
    s["chosen"] = chosen

    lines = [
        "☀️ <b>Сніданок:</b> " + chosen[0]["name"],
        "☀️ <b>Обід:</b> " + chosen[1]["name"],
        "🌙 <b>Вечеря:</b> " + chosen[2]["name"],
    ]
    msg = "🍽 <b>Ваше меню на день:</b>\n\n" + "\n".join(lines) + "\n\nНатисніть на страву, щоб отримати рецепт 👇"

    markup = types.InlineKeyboardMarkup()
    for i, dish in enumerate(chosen):
        markup.add(types.InlineKeyboardButton(dish["name"], callback_data=f"recipe_{dish['id']}"))
    bot.edit_message_text(
        msg,
        callback.message.chat.id,
        callback.message.message_id,
        reply_markup=markup,
    )
    bot.answer_callback_query(callback.id)


@bot.callback_query_handler(func=lambda c: c.data.startswith("recipe_"))
def callback_recipe(callback):
    recipe_id = callback.data.replace("recipe_", "")
    recipe = next((r for r in RECIPES if r["id"] == recipe_id), None)
    if not recipe:
        bot.answer_callback_query(callback.id)
        return
    bot.send_message(callback.message.chat.id, recipe["recipe"])
    bot.answer_callback_query(callback.id)


@bot.message_handler(func=lambda m: True)
def handle_text(message):
    s = get_state(message.chat.id)

    if s["step"] == "waiting_products" or s["step"] is None:
        products = parse_products(message.text)
        if not products:
            bot.send_message(
                message.chat.id,
                "Не вдалося розпізнати продукти. Спробуй формат:\n"
                "<code>яйця 3 шт, молоко 200 г, борошно 300 г</code>",
            )
            return

        s["products"] = products
        s["step"] = "idle"
        text = "✅ Продукти збережено:\n" + "\n".join(
            f"• {k}: {v[0]} {v[1]}" for k, v in products.items()
        )
        bot.send_message(message.chat.id, text, reply_markup=main_menu_keyboard())
        bot.send_message(
            message.chat.id,
            "Тепер натисни «Згенерувати меню», щоб отримати 3 варіанти меню на день.",
            reply_markup=main_menu_keyboard(),
        )
        return

    # Інакше — спроба розпарсити продукти з тексту
    products = parse_products(message.text)
    if products:
        s["products"] = products
        s["step"] = "idle"
        text = "✅ Продукти збережено:\n" + "\n".join(
            f"• {k}: {v[0]} {v[1]}" for k, v in products.items()
        )
        bot.send_message(message.chat.id, text, reply_markup=main_menu_keyboard())
        bot.send_message(
            message.chat.id,
            "Натисни «Згенерувати меню» для отримання варіантів.",
            reply_markup=main_menu_keyboard(),
        )
    else:
        bot.send_message(
            message.chat.id,
            "Напиши список продуктів з кількістю (напр. <code>яйця 3 шт, молоко 200 г</code>) "
            "або використовуй кнопки меню.",
            reply_markup=main_menu_keyboard(),
        )


def run():
    print("Бот WeT запущено...")
    bot.infinity_polling()


if __name__ == "__main__":
    run()
