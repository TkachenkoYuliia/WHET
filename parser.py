# -*- coding: utf-8 -*-
"""
Парсер списку продуктів від користувача.
Підтримує два формати:
1. Лише перелік: "яйця, молоко, борошно"
2. З кількістю: "яйця 3 шт, молоко 200 г"
"""
import re

# Мін. кількість для "є в наявності" (без явної кількості)
DEFAULT_QTY = 999
DEFAULT_UNIT = "г"


def parse_products(text: str) -> dict:
    """
    Парсить текст у словник {продукт: (кількість, одиниця)}.
    Без кількості: "яйця, молоко, борошно" -> продукт: (999, "г")
    З кількістю: "яйця 3 шт, молоко 200 г" -> продукт: (3, "шт")
    """
    result = {}
    text = text.strip()

    # 1. Спочатку шукаємо продукти з кількістю
    patterns = [
        r"([а-яіїєґ'\-\s]+?)\s*[-–]?\s*(\d+(?:[.,]\d+)?)\s*(шт|штук|штуки|г|грам|кг|мл)\b",
        r"([а-яіїєґ'\-\s]+?)\s*(\d+(?:[.,]\d+)?)\s*(шт|штук|штуки|г|грам|кг|мл)\b",
    ]

    def norm_unit(u):
        u = (u or "").lower()
        if u in ("шт", "штук", "штуки"):
            return "шт"
        if u in ("г", "грам", "грамів"):
            return "г"
        if u == "кг":
            return "г"
        if u == "мл":
            return "мл"
        return "г"

    for pattern in patterns:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            name = m.group(1).strip().strip(" ,\t-–:")
            qty = float(m.group(2).replace(",", "."))
            unit = norm_unit(m.group(3))
            if m.group(3) and "кг" in m.group(3).lower():
                qty *= 1000
            if len(name) > 1:
                result[name] = (qty, unit)

    # 2. Якщо є продукти з кількістю, додаємо їх і повертаємо
    if result:
        return result

    # 3. Парсимо лише перелік без кількості (через кому, пробіл, новий рядок)
    parts = re.split(r"[\n,;]+", text)
    for part in parts:
        part = part.strip()
        # Пропускаємо числа на початку/кінці
        part = re.sub(r"^\d+[.,]?\d*\s*", "", part)
        part = re.sub(r"\s*\d+[.,]?\d*\s*$", "", part)
        part = part.strip()
        if len(part) > 1 and not part.isdigit():
            result[part] = (DEFAULT_QTY, DEFAULT_UNIT)

    return result
