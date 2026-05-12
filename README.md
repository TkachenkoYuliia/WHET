# WHET — Telegram-бот для меню на день / Daily menu Telegram bot

## Українська

**Репозиторій:** https://github.com/TkachenkoYuliia/WHET

Бот **WHET** допомагає скласти варіанти меню на день з інгредієнтів, які ви вводите текстом (без кількостей). Підбір страв за правилом: мінімум **3** збіги інгредієнтів з вашого списку з інгредієнтами страви (сіль, перець, олія та масло зазвичай не враховуються).

### Можливості

- Вибір мови інтерфейсу: **українська** або **English** (`/start`, кнопка **«Мова»**).
- Кнопки: додати продукти, згенерувати меню, допомога, перелік **інгредієнтів WHET**, зміна мови.
- Введення списку **назв продуктів** (через кому або з нового рядка); підтримуються українські та англійські назви зі словника аліасів.
- Збережений список показується **обраною мовою** (українські підписи для UK, англійські для EN).
- Рецепт надсилається **українською**, якщо обрано українську, та **англійською**, якщо обрано English.
- База страв містить страви на сніданок, обід, вечерю та десерти; можна додавати нові рецепти в `recipes.py`.

### Встановлення

1. Клонування (SSH):

   ```bash
   git clone git@github.com:TkachenkoYuliia/WHET.git
   cd WHET
   ```

2. Віртуальне середовище та залежності:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Токен бота у `.env` (скопіюйте з `env.example`, якщо є):

   ```bash
   cp env.example .env
   # TG_BOT_KEY=токен_від_BotFather
   ```

### Запуск

```bash
python3 bot.py
```

### Як користуватися

1. `/start` — оберіть мову.
2. Надішліть список інгредієнтів, наприклад: `яйця, молоко, борошно, помідори` або `eggs, milk, flour, tomatoes`.
3. «Згенерувати меню» — оберіть один із трьох варіантів.
4. Натисніть страву — отримаєте рецепт обраною мовою.

---

## English

**Repository:** https://github.com/TkachenkoYuliia/WHET

The **WHET** bot suggests daily menu options from ingredient names you type (no amounts). A dish matches if at least **3** of your ingredients overlap the recipe’s main ingredients (pantry items like salt, pepper, oil, and butter are usually ignored).

### Features

- UI language: **Ukrainian** or **English** (`/start`, **Language** button).
- Reply keyboard: add products, generate menu, help, WHET ingredient list, language.
- Send a comma- or newline-separated list of ingredient names; Ukrainian and English aliases from `recipes.py` are supported.
- The saved list is shown in **your UI language** (Ukrainian labels in UK mode, English labels in EN mode).
- Recipes are sent in **English** when English is selected, otherwise in Ukrainian.
- Meals include breakfast, lunch, dinner, and dessert options defined in `recipes.py`.

### Setup

1. Clone (SSH):

   ```bash
   git clone git@github.com:TkachenkoYuliia/WHET.git
   cd WHET
   ```

2. Virtual environment and dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Put your bot token in `.env`:

   ```bash
   cp env.example .env
   # TG_BOT_KEY=your_token_from_BotFather
   ```

### Run

```bash
python3 bot.py
```

### Usage

1. `/start` — pick a language.
2. Send ingredients, e.g. `eggs, milk, flour, tomatoes`.
3. Tap **Generate menu** and pick one of three options.
4. Tap a dish name for the full recipe in the active language.

---

## Git remote (SSH)

```bash
git remote set-url origin git@github.com:TkachenkoYuliia/WHET.git
git push -u origin main
```
