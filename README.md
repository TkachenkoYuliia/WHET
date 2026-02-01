# WeT — Telegram бот для меню на день

Бот допомагає скласти збалансоване меню на день з продуктів у холодильнику.

**Репозиторій:** https://github.com/TkachenkoYuliia/WeT

## Можливості

- Меню з кнопками для зручної навігації
- Введення списку продуктів з кількістю (шт або г)
- Генерація 3 варіантів збалансованого меню (сніданок, обід, вечеря)
- Перегляд рецептів при натисканні на страву

## Встановлення

1. Клонуйте репозиторій:
   ```bash
   git clone https://github.com/TkachenkoYuliia/WeT.git
   cd WeT
   ```

2. Створіть віртуальне середовище та встановіть залежності:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # або: venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. Скопіюйте `env.example` у `.env` і вставте токен бота:
   ```bash
   cp env.example .env
   # Відредагуйте .env: TG_BOT_KEY=ваш_токен_від_BotFather
   ```

## Запуск

```bash
python bot.py
```

## Використання

1. Натисніть `/start` або "Додати продукти"
2. Напишіть список продуктів у форматі:
   ```
   яйця 3 шт, молоко 200 г, борошно 300 г, помідори 2 шт
   ```
3. Натисніть "Згенерувати меню"
4. Оберіть один з 3 варіантів меню
5. Натисніть на страву, щоб отримати рецепт

## Публікація в репозиторій

```bash
cd WeT
git init
git add .
git commit -m "WeT Telegram bot: меню з продуктів у холодильнику"
git branch -M main
git remote add origin https://github.com/TkachenkoYuliia/WeT.git
git push -u origin main
```
