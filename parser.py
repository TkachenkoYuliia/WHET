# -*- coding: utf-8 -*-
"""
Парсер списку продуктів від користувача.
Формати: "продукт кількість од", "продукт - кількість од"
Одиниці: шт, штук, г, грам, кг, мл
"""
import re


def parse_products(text: str) -> dict:
    """
    Парсить текст від користувача у словник {продукт: (кількість, одиниця)}.
    Приклади:
      "яйця 3 шт, молоко 200 г" -> {"яйця": (3, "шт"), "молоко": (200, "г")}
      "борошно 300г помідори 2шт" -> {"борошно": (300, "г"), "помідори": (2, "шт")}
    """
    result = {}
    text = text.strip()

    # Патерни для різних форматів
    # 1) "продукт число од" або "продукт числоод"
    patterns = [
        # кома/перенос як роздільник
        r"([а-яіїєґ'\-\s]+?)\s*[-–]?\s*(\d+(?:[.,]\d+)?)\s*(шт|штук|штуки|г|грам|кг|мл)\b",
        r"([а-яіїєґ'\-\s]+?)\s*(\d+(?:[.,]\d+)?)\s*(шт|штук|штуки|г|грам|кг|мл)\b",
    ]

    # Нормалізація одиниць
    def norm_unit(u):
        u = u.lower()
        if u in ("шт", "штук", "штуки"):
            return "шт"
        if u in ("г", "грам", "грамів"):
            return "г"
        if u == "кг":
            return "г"  # переводимо в грами * 1000 нижче
        if u == "мл":
            return "мл"
        return "г"

    for pattern in patterns:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            name = m.group(1).strip()
            qty = float(m.group(2).replace(",", "."))
            unit = norm_unit(m.group(3))
            if unit == "г" and m.group(3).lower() == "кг":
                qty *= 1000
            name = name.strip(" ,\t-–:")
            if len(name) > 1:
                result[name] = (qty, unit)

    # Альтернативний формат: кожен рядок "продукт кількість"
    if not result:
        lines = re.split(r"[\n,;]+", text)
        for line in lines:
            line = line.strip()
            # "продукт 123 од"
            m = re.search(r"^(.+?)\s+(\d+(?:[.,]\d+)?)\s*(шт|штук|г|грам|кг|мл)?\s*$", line, re.IGNORECASE)
            if m:
                name = m.group(1).strip()
                qty = float(m.group(2).replace(",", "."))
                unit = norm_unit(m.group(3) or "г")
                if m.group(3) and "кг" in (m.group(3) or "").lower():
                    qty *= 1000
                if len(name) > 1:
                    result[name] = (qty, unit)

    return result
