# -*- coding: utf-8 -*-
"""
Telegram бот WeT — меню на день з продуктів у холодильнику (UK / EN).
"""
import html
import os

from dotenv import load_dotenv
import telebot
from telebot import types

from parser import parse_products
from recipes import (
    get_recipes_by_ingredients,
    generate_menu_variants,
    RECIPES,
    ingredient_keys_formatted,
    recipe_title,
)

load_dotenv()
BOT_TOKEN = os.getenv("TG_BOT_KEY")
if not BOT_TOKEN:
    raise ValueError("Встановіть TG_BOT_KEY у файлі .env")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

CHOOSE_LANG_FIRST = (
    "Спочатку оберіть мову кнопками в повідомленні з /start.\n"
    "Please choose a language using the buttons in the /start message."
)

TEXT = {
    "uk": {
        "welcome": (
            "Привіт, <b>{name}</b>! 👋\n\n"
            "Я бот <b>WeT</b> — допоможу скласти збалансоване меню на день з продуктів, "
            "які ти маєш.\n\n"
            "Напиши список <b>назв продуктів</b> (без кількості), через кому або з нового рядка.\n"
            "Наприклад:\n"
            "<code>помідор, капуста, молоко, борошно, рис, банан, вівсянка, цукор</code>\n\n"
            "Кнопка «Інгредієнти WHET» показує розпізнавані назви."
        ),
        "help": (
            "ℹ️ <b>Допомога</b>\n\n"
            "1️⃣ Натисни «Додати продукти» або напиши список назв продуктів "
            "(через кому або з нового рядка), <b>без кількості</b>.\n\n"
            "2️⃣ Натисни «Згенерувати меню» — отримаєш 3 варіанти меню на день.\n\n"
            "3️⃣ Обери варіант — побачиш список страв.\n\n"
            "4️⃣ Натисни на страву — отримаєш повний рецепт.\n\n"
            "Приклад:\n<code>яйця, молоко, борошно, сир, помідори</code>"
        ),
        "btn_add": "📋 Додати продукти",
        "btn_gen": "🍽 Згенерувати меню",
        "btn_help": "ℹ️ Допомога",
        "btn_ingredients": "Інгредієнти WHET",
        "add_products_prompt": (
            "📋 Напиши список <b>назв продуктів</b> (без кількості).\n"
            "Через кому, крапку з комою або з нового рядка.\n\n"
            "Приклад:\n<code>помідор, капуста, молоко, борошно, рис</code>"
        ),
        "current_list_prefix": "\n\n<b>Поточний список:</b>\n",
        "generate_no_products": "Спочатку додай продукти — натисни «Додати продукти» або напиши список.",
        "generate_no_recipes": (
            "😔 На жаль, за твоїми продуктами не знайдено підходящих страв. "
            "Спробуй додати більше з переліку «Інгредієнти WHET»."
        ),
        "menu_intro": "🍽 Ось 3 варіанти збалансованого меню на день:\n\nОберіть варіант кнопками нижче 👇",
        "menu_variant": "Варіант {i}: {b} / {l} / {d}",
        "meal_breakfast": "Сніданок",
        "meal_lunch": "Обід",
        "meal_dinner": "Вечеря",
        "menu_your_day": "🍽 <b>Ваше меню на день:</b>\n\n",
        "menu_tap_dish": "\n\nНатисніть на страву, щоб отримати рецепт 👇",
        "products_saved": "✅ Продукти збережено:\n",
        "gen_menu_hint": "Тепер натисни «Згенерувати меню», щоб отримати 3 варіанти меню на день.",
        "gen_menu_hint_short": "Натисни «Згенерувати меню» для отримання варіантів.",
        "parse_fail": (
            "Не вдалося розпізнати продукти. Використовуй назви з переліку «Інгредієнти WHET».\n"
            "Приклад:\n<code>молоко, яйця, борошно, цукор</code>"
        ),
        "idle_hint": "Напиши список продуктів або скористайся кнопками меню.",
        "ingredients_title": "🥄 <b>Інгредієнти WHET</b> (канонічні назви, які бот розпізнає):",
        "ingredients_footer": "\n\nТакож підходять синоніми та англійські назви зі словника аліасів.",
    },
    "en": {
        "welcome": (
            "Hi, <b>{name}</b>! 👋\n\n"
            "I'm the <b>WeT</b> bot — I'll help you plan a balanced day from what you have.\n\n"
            "Send a list of <b>ingredient names</b> (no amounts), separated by commas or new lines.\n"
            "Example:\n"
            "<code>tomato, cabbage, milk, flour, rice, banana, oats, sugar</code>\n\n"
            "Use “WHET Ingredients” to see recognized names."
        ),
        "help": (
            "ℹ️ <b>Help</b>\n\n"
            "1️⃣ Tap “Add products” or send a list of ingredient names "
            "(comma or new line), <b>without amounts</b>.\n\n"
            "2️⃣ Tap “Generate menu” — you'll get 3 daily menu options.\n\n"
            "3️⃣ Pick an option — you'll see the dishes.\n\n"
            "4️⃣ Tap a dish — you'll get the full recipe.\n\n"
            "Example:\n<code>eggs, milk, flour, cheese, tomatoes</code>"
        ),
        "btn_add": "📋 Add products",
        "btn_gen": "🍽 Generate menu",
        "btn_help": "ℹ️ Help",
        "btn_ingredients": "🥄 WHET Ingredients",
        "add_products_prompt": (
            "📋 Send a list of <b>ingredient names</b> (no amounts).\n"
            "Separate with commas, semicolons, or new lines.\n\n"
            "Example:\n<code>tomato, cabbage, milk, flour, rice</code>"
        ),
        "current_list_prefix": "\n\n<b>Current list:</b>\n",
        "generate_no_products": "Add products first — tap “Add products” or send a list.",
        "generate_no_recipes": (
            "😔 No matching dishes for those products. "
            "Try adding more names from “WHET Ingredients”."
        ),
        "menu_intro": "🍽 Here are 3 balanced menu options for the day:\n\nPick one below 👇",
        "menu_variant": "Option {i}: {b} / {l} / {d}",
        "meal_breakfast": "Breakfast",
        "meal_lunch": "Lunch",
        "meal_dinner": "Dinner",
        "menu_your_day": "🍽 <b>Your menu for the day:</b>\n\n",
        "menu_tap_dish": "\n\nTap a dish for the full recipe 👇",
        "products_saved": "✅ Saved products:\n",
        "gen_menu_hint": "Now tap “Generate menu” to get 3 daily options.",
        "gen_menu_hint_short": "Tap “Generate menu” to get options.",
        "parse_fail": (
            "Couldn't recognize products. Use names from “WHET Ingredients”.\n"
            "Example:\n<code>milk, eggs, flour, sugar</code>"
        ),
        "idle_hint": "Send a product list or use the menu buttons.",
        "ingredients_title": "🥄 <b>WHET Ingredients</b> (canonical names the bot understands):",
        "ingredients_footer": "\n\nSynonyms and English aliases from the dictionary also work.",
    },
}

user_state = {}


def get_state(chat_id):
    if chat_id not in user_state:
        user_state[chat_id] = {
            "step": "choose_lang",
            "lang": None,
            "products": {},
            "variants": [],
            "chosen": None,
        }
    return user_state[chat_id]


def main_menu_keyboard(lang: str):
    t = TEXT[lang]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(t["btn_add"]), types.KeyboardButton(t["btn_gen"]))
    markup.add(types.KeyboardButton(t["btn_help"]), types.KeyboardButton(t["btn_ingredients"]))
    return markup


def _lang_ok(s) -> bool:
    return s.get("lang") in ("uk", "en")


@bot.callback_query_handler(func=lambda c: c.data in ("lang_uk", "lang_en"))
def callback_choose_language(callback):
    lang = "uk" if callback.data == "lang_uk" else "en"
    s = get_state(callback.message.chat.id)
    s["lang"] = lang
    s["step"] = "idle"
    bot.answer_callback_query(callback.id)
    try:
        bot.edit_message_reply_markup(
            callback.message.chat.id,
            callback.message.message_id,
            reply_markup=None,
        )
    except Exception:
        pass
    fn = callback.from_user.first_name or ("User" if lang == "en" else "Користувач")
    msg = TEXT[lang]["welcome"].format(name=html.escape(fn))
    bot.send_message(callback.message.chat.id, msg, reply_markup=main_menu_keyboard(lang))


@bot.message_handler(commands=["start"])
def cmd_start(message):
    s = get_state(message.chat.id)
    s["step"] = "choose_lang"
    s["lang"] = None
    s["products"] = {}
    s["variants"] = []
    s["chosen"] = None
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("Українська", callback_data="lang_uk"),
        types.InlineKeyboardButton("English", callback_data="lang_en"),
    )
    bot.send_message(
        message.chat.id,
        "Оберіть мову / <b>Choose language</b>",
        reply_markup=markup,
    )


@bot.message_handler(commands=["help"])
def cmd_help(message):
    s = get_state(message.chat.id)
    if not _lang_ok(s):
        bot.send_message(message.chat.id, CHOOSE_LANG_FIRST)
        return
    bot.send_message(
        message.chat.id,
        TEXT[s["lang"]]["help"],
        reply_markup=main_menu_keyboard(s["lang"]),
    )


@bot.message_handler(func=lambda m: m.text in (TEXT["uk"]["btn_help"], TEXT["en"]["btn_help"]))
def btn_help(message):
    cmd_help(message)


@bot.message_handler(
    func=lambda m: m.text in (TEXT["uk"]["btn_ingredients"], TEXT["en"]["btn_ingredients"])
)
def btn_ingredients(message):
    s = get_state(message.chat.id)
    if not _lang_ok(s):
        bot.send_message(message.chat.id, CHOOSE_LANG_FIRST)
        return
    lang = s["lang"]
    body = TEXT[lang]["ingredients_title"] + "\n\n" + ingredient_keys_formatted()
    body += TEXT[lang]["ingredients_footer"]
    bot.send_message(message.chat.id, body, reply_markup=main_menu_keyboard(lang))


@bot.message_handler(func=lambda m: m.text in (TEXT["uk"]["btn_add"], TEXT["en"]["btn_add"]))
def btn_add_products(message):
    s = get_state(message.chat.id)
    if not _lang_ok(s):
        bot.send_message(message.chat.id, CHOOSE_LANG_FIRST)
        return
    lang = s["lang"]
    s["step"] = "waiting_products"
    extra = ""
    if s["products"]:
        extra = TEXT[lang]["current_list_prefix"] + ", ".join(s["products"].keys())
    bot.send_message(
        message.chat.id,
        TEXT[lang]["add_products_prompt"] + extra,
    )


@bot.message_handler(func=lambda m: m.text in (TEXT["uk"]["btn_gen"], TEXT["en"]["btn_gen"]))
def btn_generate(message):
    s = get_state(message.chat.id)
    if not _lang_ok(s):
        bot.send_message(message.chat.id, CHOOSE_LANG_FIRST)
        return
    lang = s["lang"]
    if not s["products"]:
        bot.send_message(
            message.chat.id,
            TEXT[lang]["generate_no_products"],
            reply_markup=main_menu_keyboard(lang),
        )
        return

    recipes = get_recipes_by_ingredients(s["products"])
    if not recipes:
        bot.send_message(
            message.chat.id,
            TEXT[lang]["generate_no_recipes"],
            reply_markup=main_menu_keyboard(lang),
        )
        return

    variants = generate_menu_variants(recipes, 3)
    s["variants"] = variants
    s["step"] = "choose_menu"

    markup = types.InlineKeyboardMarkup()
    for i, v in enumerate(variants, 1):
        b, l, d = v[0], v[1], v[2]
        label = TEXT[lang]["menu_variant"].format(
            i=i,
            b=recipe_title(b, lang),
            l=recipe_title(l, lang),
            d=recipe_title(d, lang),
        )
        markup.add(types.InlineKeyboardButton(label, callback_data=f"menu_{i}"))
    bot.send_message(message.chat.id, TEXT[lang]["menu_intro"], reply_markup=markup)


@bot.callback_query_handler(func=lambda c: c.data.startswith("menu_"))
def callback_choose_menu(callback):
    idx = int(callback.data.split("_")[1])
    s = get_state(callback.message.chat.id)
    if not _lang_ok(s) or not s["variants"] or idx < 1 or idx > len(s["variants"]):
        bot.answer_callback_query(callback.id)
        return

    lang = s["lang"]
    chosen = s["variants"][idx - 1]
    s["chosen"] = chosen

    lines = [
        f"☀️ <b>{TEXT[lang]['meal_breakfast']}:</b> " + recipe_title(chosen[0], lang),
        f"☀️ <b>{TEXT[lang]['meal_lunch']}:</b> " + recipe_title(chosen[1], lang),
        f"🌙 <b>{TEXT[lang]['meal_dinner']}:</b> " + recipe_title(chosen[2], lang),
    ]
    msg = TEXT[lang]["menu_your_day"] + "\n".join(lines) + TEXT[lang]["menu_tap_dish"]

    markup = types.InlineKeyboardMarkup()
    for dish in chosen:
        markup.add(
            types.InlineKeyboardButton(recipe_title(dish, lang), callback_data=f"recipe_{dish['id']}")
        )
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

    if s["step"] == "choose_lang" or not _lang_ok(s):
        bot.send_message(message.chat.id, CHOOSE_LANG_FIRST)
        return

    lang = s["lang"]

    if s["step"] == "waiting_products":
        products = parse_products(message.text)
        if not products:
            bot.send_message(message.chat.id, TEXT[lang]["parse_fail"])
            return

        s["products"] = products
        s["step"] = "idle"
        text = TEXT[lang]["products_saved"] + "\n".join(f"• {k}" for k in products.keys())
        bot.send_message(message.chat.id, text, reply_markup=main_menu_keyboard(lang))
        bot.send_message(message.chat.id, TEXT[lang]["gen_menu_hint"], reply_markup=main_menu_keyboard(lang))
        return

    products = parse_products(message.text)
    if products:
        s["products"] = products
        s["step"] = "idle"
        text = TEXT[lang]["products_saved"] + "\n".join(f"• {k}" for k in products.keys())
        bot.send_message(message.chat.id, text, reply_markup=main_menu_keyboard(lang))
        bot.send_message(message.chat.id, TEXT[lang]["gen_menu_hint_short"], reply_markup=main_menu_keyboard(lang))
    else:
        bot.send_message(
            message.chat.id,
            TEXT[lang]["idle_hint"],
            reply_markup=main_menu_keyboard(lang),
        )


def run():
    print("Бот WeT запущено...")
    bot.infinity_polling()


if __name__ == "__main__":
    run()
