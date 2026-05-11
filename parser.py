# -*- coding: utf-8 -*-
"""
Парсер списку продуктів від користувача (лише назви, без кількостей).
Розділювачі: кома, крапка з комою, перенос рядка.
Підтримуються слова латиницею та кирилицею (див. INGREDIENT_ALIASES у recipes).
"""
import re

from recipes import normalize_ingredient


def parse_products(text: str) -> dict:
    """
    Повертає словник {канонічна_назва: (1.0, "шт")} для розпізнаних інгредієнтів.
    Приклад: "помідор, капуста, milk, rice" → {"помідори": (1.0, "шт"), ...}
    """
    result: dict[str, tuple[float, str]] = {}
    text = (text or "").strip()
    if not text:
        return result

    def add_norm(norm: str | None) -> None:
        if norm and len(norm) > 1:
            result[norm] = (1.0, "шт")

    for raw in re.split(r"[\n,;]+", text):
        chunk = raw.strip().strip(" \t.")
        if not chunk:
            continue
        whole = normalize_ingredient(chunk)
        if whole:
            add_norm(whole)
            continue
        for token in re.findall(r"[a-zа-яіїєґ'\-]+", chunk.lower()):
            add_norm(normalize_ingredient(token))

    if not result:
        for token in re.findall(r"[a-zа-яіїєґ'\-]+", text.lower()):
            add_norm(normalize_ingredient(token))

    return result
