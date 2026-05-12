# -*- coding: utf-8 -*-
"""
База рецептів для бота WeT.
Кожен рецепт має: інгредієнти (продукт: мін. кількість у грамах або штуках),
тип прийому їжі, назву та інструкцію приготування.
"""

# Словник для нормалізації назв продуктів (різні варіанти -> однакова назва)
INGREDIENT_ALIASES = {
    "яйця": ["яйце", "яйця", "яйцю", "яєць", "egg", "eggs"],
    "молоко": ["молоко", "молока", "milk"],
    "борошно": ["борошно", "мука", "flour"],
    "масло": ["масло", "вершкове масло", "butter"],
    "олія": ["олія", "рослинна олія", "vegetable oil", "sunflower oil"],
    "цукор": ["цукор", "цукру", "sugar"],
    "сіль": ["сіль", "солі", "salt"],
    "перець": ["перець", "чорний перець", "pepper", "black pepper"],
    "помідори": ["помідор", "помідори", "помідорів", "tomato", "tomatoes"],
    "огірки": ["огірок", "огірки", "огірків", "cucumber", "cucumbers", "pickles"],
    "картопля": ["картопля", "картоплі", "potato", "potatoes"],
    "цибуля": ["цибуля", "цибули", "лук", "onion", "onions"],
    "часник": ["часник", "часнику", "garlic"],
    "морква": ["морква", "моркви", "carrot", "carrots"],
    "курка": ["курка", "курки", "курятина", "курицею", "chicken"],
    "м'ясо": ["м'ясо", "м'яса", "свинина", "яловичина", "meat", "beef", "pork"],
    "сир": ["сир", "сиру", "твердий сир", "творог", "творогу", "cheese", "cottage cheese", "tvorog"],
    "вершки": ["вершки", "сметана", "cream"],
    "сметана": ["сметана", "сметани", "sour cream"],
    "рис": ["рис", "рису", "rice"],
    "макарони": ["макарони", "паста", "спагеті", "pasta", "spaghetti", "macaroni"],
    "яблука": ["яблуко", "яблука", "apple", "apples"],
    "банан": ["банан", "банани", "banana", "bananas"],
    "лимон": ["лимон", "лимони", "лимонний сік", "lemon", "lemons", "lemon juice"],
    "зелень": ["зелень", "петрушка", "кріп", "базилік", "herbs", "parsley", "dill", "basil"],
    "хліб": ["хліб", "батон", "bread", "loaf"],
    "йогурт": ["йогурт", "йогурту", "yogurt", "yoghurt"],
    "ковбаса": ["ковбаса", "ковбаси", "sausage", "salami"],
    "яйце": ["яйце", "яйця", "egg", "eggs"],
    "вівсянка": ["вівсянка", "вівсяні пластівці", "овсянка", "oats", "oat", "oatmeal", "rolled oats"],
    "буряк": ["буряк", "буряка", "свекла", "beet", "beetroot"],
    "капуста": ["капуста", "капусти", "cabbage"],
    "оливки": ["оливки", "маслини", "olives"],
    "гречка": ["гречка", "гречки", "гречана крупа", "buckwheat"],
    "лапша": ["лапша", "лапші", "noodles", "noodle", "egg noodles"],
    "тунець": ["тунець", "тунця", "tuna"],
    "риба": ["риба", "риби", "fish", "fillet"],
    "гриби": ["гриби", "грибів", "mushrooms", "mushroom"],
    "болгарський перець": [
        "болгарський перець",
        "перець болгарський",
        "sweet pepper",
        "bell pepper",
        "paprika",
    ],
    "кукурудза": ["кукурудза", "кукурудзи", "corn", "sweet corn"],
    "квасоля": ["квасоля", "квасолі", "beans", "kidney beans", "white beans"],
    "горошок": ["горошок", "горошку", "peas", "green peas"],
    "соєвий соус": ["соєвий соус", "соус соєвий", "soy sauce"],
    "мед": ["мед", "меду", "honey"],
    "варення": ["варення", "jam", "berry jam"],
    "шоколад": ["шоколад", "chocolate"],
    "какао": ["какао", "cocoa", "cocoa powder"],
    "ягоди": ["ягоди", "ягід", "berries", "berry"],
    "шпинат": ["шпинат", "шпинату", "spinach"],
    "баклажан": ["баклажан", "баклажана", "eggplant", "aubergine"],
    "кабачок": ["кабачок", "кабачка", "zucchini", "courgette"],
}

# Підписи для відповіді користувачу (канонічний ключ → текст)
INGREDIENT_LABEL_UK = {k: k for k in INGREDIENT_ALIASES}

INGREDIENT_LABEL_EN = {
    "яйця": "egg",
    "молоко": "milk",
    "борошно": "flour",
    "масло": "butter",
    "олія": "oil",
    "цукор": "sugar",
    "сіль": "salt",
    "перець": "pepper",
    "помідори": "tomato",
    "огірки": "cucumber",
    "картопля": "potato",
    "цибуля": "onion",
    "часник": "garlic",
    "морква": "carrot",
    "курка": "chicken",
    "м'ясо": "meat",
    "сир": "cheese",
    "вершки": "cream",
    "сметана": "sour cream",
    "рис": "rice",
    "макарони": "pasta",
    "яблука": "apple",
    "банан": "banana",
    "лимон": "lemon",
    "зелень": "herbs",
    "хліб": "bread",
    "йогурт": "yogurt",
    "ковбаса": "sausage",
    "яйце": "egg",
    "вівсянка": "oat",
    "буряк": "beet",
    "капуста": "cabbage",
    "оливки": "olives",
    "гречка": "buckwheat",
    "лапша": "noodles",
    "тунець": "tuna",
    "риба": "fish",
    "гриби": "mushroom",
    "болгарський перець": "bell pepper",
    "кукурудза": "corn",
    "квасоля": "beans",
    "горошок": "peas",
    "соєвий соус": "soy sauce",
    "мед": "honey",
    "варення": "jam",
    "шоколад": "chocolate",
    "какао": "cocoa",
    "ягоди": "berries",
    "шпинат": "spinach",
    "баклажан": "eggplant",
    "кабачок": "zucchini",
}


def ingredient_display(canonical: str, lang: str) -> str:
    if lang == "en":
        return INGREDIENT_LABEL_EN.get(canonical, canonical)
    return INGREDIENT_LABEL_UK.get(canonical, canonical)


def ingredient_catalog_formatted(lang: str) -> str:
    return "\n".join(
        f"• {ingredient_display(k, lang)}" for k in sorted(INGREDIENT_ALIASES.keys())
    )


def recipe_body(recipe: dict, lang: str) -> str:
    if lang == "en" and recipe.get("recipe_en"):
        return recipe["recipe_en"]
    return recipe["recipe"]


# Рецепти: інгредієнти задані як (назва: мін. кількість)
# Кількість: для "шт" - штуки, для "г" - грами
RECIPES = [
    {
        "id": "omlet",
        "name": "Омлет",
        "name_en": "Omelette",
        "meal_type": "breakfast",
        "ingredients": {"яйця": (2, "шт"), "молоко": (30, "г"), "сіль": (1, "г"), "масло": (10, "г")},
        "recipe": """🍳 ОМЛЕТ

Інгредієнти:
• 2-3 яйця
• 30-50 мл молока
• Сіль за смаком
• 10 г вершкового масла

Приготування:
1. Збийте яйця з молоком та сіллю.
2. Розігрійте сковороду з маслом.
3. Вилийте суміш, накрийте кришкою.
4. Готуйте на середньому вогні 3-4 хв до зарум'янення.
5. Переверніть або складіть пополам. Готово!""",
        "recipe_en": """🍳 OMELETTE

Ingredients:
• 2–3 eggs
• 30–50 ml milk
• Salt to taste
• 10 g butter

Steps:
1. Beat eggs with milk and salt.
2. Heat a pan with butter.
3. Pour in the mixture, cover with a lid.
4. Cook on medium heat for 3–4 minutes until golden.
5. Flip or fold in half. Done!""",
    },
    {
        "id": "syrnyky",
        "name": "Сирники",
        "name_en": "Syrniki (cheese pancakes)",
        "meal_type": "breakfast",
        "ingredients": {"сир": (200, "г"), "яйця": (1, "шт"), "борошно": (50, "г"), "цукор": (20, "г"), "сіль": (1, "г"), "олія": (30, "г")},
        "recipe": """🥞 СИРНИКИ

Інгредієнти:
• 200 г сиру
• 1 яйце
• 2-3 ст. л. борошна
• 1 ст. л. цукру
• Щіпка солі
• Олія для смаження

Приготування:
1. Змішайте сир, яйце, цукор, сіль.
2. Додайте борошно, замісіть тісто.
3. Сформуйте круглі сирники.
4. Обсмажте на олії з обох боків до золотистої скоринки.
5. Подавайте зі сметаною або варенням.""",
        "recipe_en": """🥞 SYRNIKI (CHEESE PANCAKES)

Ingredients:
• 200 g cottage cheese / soft farmer’s cheese
• 1 egg
• 2–3 tbsp flour
• 1 tbsp sugar
• Pinch of salt
• Oil for frying

Steps:
1. Mix cheese, egg, sugar, and salt.
2. Add flour and mix into a soft dough.
3. Shape into small patties.
4. Fry in oil on both sides until golden.
5. Serve with sour cream or jam.""",
    },
    {
        "id": "vivsianka",
        "name": "Вівсянка з бананом",
        "name_en": "Oatmeal with banana",
        "meal_type": "breakfast",
        "ingredients": {"вівсянка": (50, "г"), "молоко": (150, "г"), "банан": (1, "шт"), "цукор": (10, "г")},
        "recipe": """🥣 ВІВСЯНКА З БАНАНОМ

Інгредієнти:
• 50 г вівсяних пластівців
• 150 мл молока
• 1 банан
• Цукор або мед за смаком

Приготування:
1. Доведіть молоко до кипіння.
2. Додайте вівсянку, варіть 3-5 хв, помішуючи.
3. Наріжте банан, додайте до каші.
4. Підсолодіть за бажанням. Готово!""",
        "recipe_en": """🥣 OATMEAL WITH BANANA

Ingredients:
• 50 g rolled oats
• 150 ml milk
• 1 banana
• Sugar or honey to taste

Steps:
1. Bring milk to a boil.
2. Add oats, cook 3–5 minutes, stirring.
3. Slice the banana and stir into the porridge.
4. Sweeten if you like. Done!""",
    },
    {
        "id": "sandwich",
        "name": "Сендвіч з яйцем",
        "name_en": "Egg sandwich",
        "meal_type": "breakfast",
        "ingredients": {"хліб": (2, "шт"), "яйця": (1, "шт"), "масло": (10, "г"), "сіль": (1, "г")},
        "recipe": """🥪 СЕНДВІЧ З ЯЙЦЕМ

Інгредієнти:
• 2 скибочки хліба
• 1 яйце
• 10 г вершкового масла
• Сіль за смаком

Приготування:
1. Зваріть яйце вкруту.
2. Намажте хліб маслом.
3. Наріжте яйце, покладіть на хліб.
4. Посоліть. Можна додати зелень.""",
        "recipe_en": """🥪 EGG SANDWICH

Ingredients:
• 2 slices of bread
• 1 egg
• 10 g butter
• Salt to taste

Steps:
1. Hard-boil the egg.
2. Butter the bread.
3. Slice the egg and place on the bread.
4. Season with salt. Add herbs if you like.""",
    },
    {
        "id": "borshch",
        "name": "Борщ",
        "name_en": "Borscht",
        "meal_type": "lunch",
        "ingredients": {"буряк": (100, "г"), "картопля": (150, "г"), "капуста": (100, "г"), "морква": (50, "г"), "цибуля": (30, "г"), "м'ясо": (100, "г"), "сметана": (30, "г"), "сіль": (5, "г")},
        "recipe": """🍲 БОРЩ

Інгредієнти:
• 100 г буряка
• 150 г картоплі
• 100 г капусти
• 50 г моркви
• 30 г цибулі
• 100 г м'яса
• Сметана, сіль, перець

Приготування:
1. Варіть м'ясо до готовності.
2. Додайте нарізану картоплю та капусту.
3. Підсмажте цибулю, моркву, буряк.
4. Додайте засмажку до борщу.
5. Варіть 10-15 хв. Подавайте зі сметаною.""",
        "recipe_en": """🍲 BORSCHT

Ingredients:
• 100 g beet
• 150 g potato
• 100 g cabbage
• 50 g carrot
• 30 g onion
• 100 g meat
• Sour cream, salt, pepper

Steps:
1. Simmer meat until tender.
2. Add chopped potato and cabbage.
3. Sauté onion, carrot, and beet.
4. Add the sautéed vegetables to the soup.
5. Simmer 10–15 minutes. Serve with sour cream.""",
    },
    {
        "id": "solyanka",
        "name": "Солянка",
        "name_en": "Solyanka",
        "meal_type": "lunch",
        "ingredients": {"м'ясо": (80, "г"), "ковбаса": (50, "г"), "огірки": (50, "г"), "помідори": (50, "г"), "цибуля": (30, "г"), "оливки": (20, "г"), "сметана": (30, "г"), "лимон": (10, "г")},
        "recipe": """🍜 СОЛЯНКА

Інгредієнти:
• 80 г вареного м'яса
• 50 г ковбаси
• 50 г солених огірків
• 50 г помідорів
• Цибуля, оливки, лимон
• Сметана

Приготування:
1. Зробіть м'ясний бульйон.
2. Додайте нарізані м'ясо, ковбасу, огірки, помідори.
3. Підсмажте цибулю.
4. Варіть 10 хв. Додайте оливки, лимон.
5. Подавайте зі сметаною.""",
        "recipe_en": """🍜 SOLYANKA

Ingredients:
• 80 g cooked meat
• 50 g sausage
• 50 g pickled cucumbers
• 50 g tomatoes
• Onion, olives, lemon
• Sour cream

Steps:
1. Make a meat broth.
2. Add diced meat, sausage, cucumbers, and tomatoes.
3. Sauté onion and add to the pot.
4. Simmer ~10 minutes; add olives and a squeeze of lemon.
5. Serve with sour cream.""",
    },
    {
        "id": "kotleta",
        "name": "Котлети з куркою",
        "name_en": "Chicken cutlets",
        "meal_type": "lunch",
        "ingredients": {"курка": (200, "г"), "цибуля": (50, "г"), "яйця": (1, "шт"), "борошно": (30, "г"), "сіль": (3, "г"), "олія": (30, "г")},
        "recipe": """🍗 КОТЛЕТИ З КУРКОЮ

Інгредієнти:
• 200 г курячого фаршу
• 50 г цибулі
• 1 яйце
• 2 ст. л. борошна
• Сіль, перець
• Олія для смаження

Приготування:
1. Змішайте фарш з цибулею, яйцем, сіллю.
2. Сформуйте котлети, обваляйте в борошні.
3. Смажте на олії з обох боків до золотистої скоринки.
4. Можна потушити під кришкою 5-7 хв.""",
        "recipe_en": """🍗 CHICKEN CUTLETS

Ingredients:
• 200 g ground chicken
• 50 g onion
• 1 egg
• 2 tbsp flour
• Salt, pepper
• Oil for frying

Steps:
1. Mix ground chicken with grated onion, egg, and salt.
2. Shape into patties and lightly coat with flour.
3. Fry in oil on both sides until golden.
4. Optionally cover and simmer 5–7 minutes.""",
    },
    {
        "id": "ris_kurka",
        "name": "Рис з куркою",
        "name_en": "Rice with chicken",
        "meal_type": "lunch",
        "ingredients": {"рис": (80, "г"), "курка": (100, "г"), "морква": (50, "г"), "цибуля": (30, "г"), "олія": (20, "г"), "сіль": (3, "г")},
        "recipe": """🍚 РИС З КУРКОЮ

Інгредієнти:
• 80 г рису
• 100 г курки
• 50 г моркви
• 30 г цибулі
• Олія, сіль, перець

Приготування:
1. Підсмажте курку з цибулею та морквою.
2. Додайте промитий рис, залийте водою (1:2).
3. Доведіть до кипіння, зменшіть вогонь.
4. Накрийте кришкою, варіть 15-20 хв.
5. Перемішайте, дайте настоятися.""",
        "recipe_en": """🍚 RICE WITH CHICKEN

Ingredients:
• 80 g rice
• 100 g chicken
• 50 g carrot, 30 g onion
• Oil, salt, pepper

Steps:
1. Sauté chicken with onion and carrot.
2. Add rinsed rice and water (about 1:2 ratio).
3. Bring to a boil, reduce heat.
4. Cover and cook 15–20 minutes.
5. Rest off heat, then fluff.""",
    },
    {
        "id": "pasta",
        "name": "Паста з томатним соусом",
        "name_en": "Pasta with tomato sauce",
        "meal_type": "lunch",
        "ingredients": {"макарони": (100, "г"), "помідори": (100, "г"), "цибуля": (30, "г"), "часник": (5, "г"), "олія": (20, "г"), "сіль": (3, "г"), "сир": (30, "г")},
        "recipe": """🍝 ПАСТА З ТОМАТНИМ СОУСОМ

Інгредієнти:
• 100 г макарон
• 100 г помідорів
• Цибуля, часник
• Олія, сіль, базилік
• 30 г сиру

Приготування:
1. Варіть макарони до готовності.
2. Підсмажте цибулю з часником.
3. Додайте помідори, тушкуйте 5-7 хв.
4. Змішайте з відкинутими макаронами.
5. Посипте сиром та зеленню.""",
        "recipe_en": """🍝 PASTA WITH TOMATO SAUCE

Ingredients:
• 100 g pasta
• 100 g tomatoes
• Onion, garlic
• Oil, salt, basil
• 30 g cheese

Steps:
1. Boil pasta until al dente.
2. Sauté onion and garlic.
3. Add tomatoes and simmer 5–7 minutes.
4. Toss with drained pasta.
5. Top with cheese and herbs.""",
    },
    {
        "id": "salat_ovoch",
        "name": "Салат з овочів",
        "name_en": "Vegetable salad",
        "meal_type": "lunch",
        "ingredients": {"помідори": (50, "г"), "огірки": (50, "г"), "цибуля": (20, "г"), "олія": (15, "г"), "сіль": (2, "г"), "зелень": (10, "г")},
        "recipe": """🥗 САЛАТ З ОВОЧІВ

Інгредієнти:
• 50 г помідорів
• 50 г огірків
• 20 г цибулі
• Олія, сіль, зелень

Приготування:
1. Наріжте помідори та огірки.
2. Додайте дрібно нарізану цибулю.
3. Заправте олією, посоліть.
4. Прикрасьте зеленню.""",
        "recipe_en": """🥗 VEGETABLE SALAD

Ingredients:
• 50 g tomatoes
• 50 g cucumbers
• 20 g onion
• Oil, salt, herbs

Steps:
1. Dice tomatoes and cucumbers.
2. Add finely chopped onion.
3. Dress with oil and salt.
4. Garnish with herbs.""",
    },
    {
        "id": "kasha_grech",
        "name": "Гречка з м'ясом",
        "name_en": "Buckwheat with meat",
        "meal_type": "dinner",
        "ingredients": {"гречка": (80, "г"), "м'ясо": (100, "г"), "цибуля": (30, "г"), "морква": (30, "г"), "олія": (20, "г"), "сіль": (3, "г")},
        "recipe": """🍛 ГРЕЧКА З М'ЯСОМ

Інгредієнти:
• 80 г гречки
• 100 г м'яса
• Цибуля, морква
• Олія, сіль, перець

Приготування:
1. Підсмажте м'ясо з цибулею та морквою.
2. Додайте промиту гречку, залийте водою.
3. Доведіть до кипіння, зменшіть вогонь.
4. Варіть 15-20 хв під кришкою.
5. Дайте настоятися.""",
        "recipe_en": """🍛 BUCKWHEAT WITH MEAT

Ingredients:
• 80 g buckwheat
• 100 g meat
• Onion, carrot
• Oil, salt, pepper

Steps:
1. Sauté meat with onion and carrot.
2. Add rinsed buckwheat and water.
3. Bring to a boil, reduce heat.
4. Simmer 15–20 minutes covered.
5. Rest before serving.""",
    },
    {
        "id": "omlet_veg",
        "name": "Омлет з овочами",
        "name_en": "Vegetable omelette",
        "meal_type": "dinner",
        "ingredients": {"яйця": (2, "шт"), "помідори": (50, "г"), "огірки": (30, "г"), "сир": (30, "г"), "олія": (15, "г"), "сіль": (2, "г")},
        "recipe": """🥘 ОМЛЕТ З ОВОЧАМИ

Інгредієнти:
• 2 яйця
• 50 г помідорів
• 30 г огірків
• 30 г сиру
• Олія, сіль

Приготування:
1. Збийте яйця з сіллю.
2. Підсмажте дрібно нарізані овочі.
3. Залейте яєчною сумішшю.
4. Посипте сиром, накрийте кришкою.
5. Готуйте 3-4 хв на повільному вогні.""",
        "recipe_en": """🥘 VEGETABLE OMELETTE

Ingredients:
• 2 eggs
• 50 g tomatoes
• 30 g cucumber
• 30 g cheese
• Oil, salt

Steps:
1. Beat eggs with salt.
2. Sauté diced vegetables briefly.
3. Pour in the egg mixture.
4. Sprinkle cheese, cover with a lid.
5. Cook 3–4 minutes on low heat.""",
    },
    {
        "id": "sup_kurka",
        "name": "Курячий суп з лапшею",
        "name_en": "Chicken noodle soup",
        "meal_type": "dinner",
        "ingredients": {"курка": (100, "г"), "картопля": (100, "г"), "морква": (50, "г"), "цибуля": (30, "г"), "лапша": (50, "г"), "сіль": (3, "г"), "зелень": (10, "г")},
        "recipe": """🍜 КУРЯЧИЙ СУП З ЛАПШЕЮ

Інгредієнти:
• 100 г курки
• 100 г картоплі
• 50 г моркви, 30 г цибулі
• 50 г лапши
• Сіль, зелень

Приготування:
1. Варіть курку до готовності.
2. Додайте картоплю, моркву, цибулю.
3. Варіть 10 хв, додайте лапшу.
4. Варіть ще 5-7 хв.
5. Посипте зеленню.""",
        "recipe_en": """🍜 CHICKEN NOODLE SOUP

Ingredients:
• 100 g chicken
• 100 g potato
• 50 g carrot, 30 g onion
• 50 g noodles
• Salt, herbs

Steps:
1. Simmer chicken until cooked.
2. Add potato, carrot, and onion.
3. Cook ~10 minutes, add noodles.
4. Simmer 5–7 minutes more.
5. Garnish with herbs.""",
    },
    {
        "id": "tворог",
        "name": "Творог з ягодами",
        "name_en": "Cottage cheese with fruit",
        "meal_type": "dinner",
        "ingredients": {"сир": (150, "г"), "йогурт": (50, "г"), "банан": (50, "г"), "цукор": (10, "г")},
        "recipe": """🥄 ТВОРОГ З ЯГОДАМИ

Інгредієнти:
• 150 г творогу
• 50 г йогурту
• Банан або ягоди
• Цукор або мед

Приготування:
1. Змішайте творог з йогуртом.
2. Додайте нарізаний банан або ягоди.
3. Підсолодіть за смаком.""",
        "recipe_en": """🥄 COTTAGE CHEESE WITH FRUIT

Ingredients:
• 150 g cottage cheese
• 50 g yogurt
• Banana or berries
• Sugar or honey

Steps:
1. Mix cottage cheese with yogurt.
2. Add sliced banana or berries.
3. Sweeten to taste.""",
    },
    {
        "id": "salat_tunets",
        "name": "Салат з тунцем",
        "name_en": "Tuna salad",
        "meal_type": "lunch",
        "ingredients": {"тунець": (80, "г"), "цибуля": (30, "г"), "морква": (40, "г"), "лимон": (10, "г"), "олія": (15, "г"), "сіль": (2, "г")},
        "recipe": """🐟 САЛАТ З ТУНЦЕМ

Інгредієнти:
• 80 г тунця (консервованого)
• Цибуля, морква
• Лимонний сік, олія, сіль

Приготування:
1. Злийте рідину з тунця, розімніть виделкою.
2. Додайте дрібно нарізану цибулю та терту моркву.
3. Заправте олією, лимоном, сіллю. Подавайте охолодженим.""",
        "recipe_en": """🐟 TUNA SALAD

Ingredients:
• 80 g canned tuna (drained)
• Onion, carrot
• Lemon juice, oil, salt

Steps:
1. Drain tuna and flake with a fork.
2. Add finely diced onion and grated carrot.
3. Dress with oil, lemon, and salt. Serve chilled.""",
    },
    {
        "id": "pure_kartop_kurka",
        "name": "Картопляне пюре з куркою",
        "name_en": "Mashed potato with chicken",
        "meal_type": "dinner",
        "ingredients": {"картопля": (300, "г"), "курка": (120, "г"), "молоко": (80, "г"), "масло": (20, "г"), "сіль": (3, "г")},
        "recipe": """🥔 КАРТОПЛЯНЕ ПЮРЕ З КУРКОЮ

Інгредієнти:
• 300 г картоплі
• 120 г курячого філе
• 80 мл молока, 20 г масла, сіль

Приготування:
1. Відваріть картоплю, розімніть з молоком і маслом.
2. Обсмажте курку до готовності, наріжте.
3. Подавайте пюре з шматочками курки.""",
        "recipe_en": """🥔 MASHED POTATO WITH CHICKEN

Ingredients:
• 300 g potatoes
• 120 g chicken fillet
• 80 ml milk, 20 g butter, salt

Steps:
1. Boil potatoes, mash with milk and butter.
2. Pan-fry chicken until cooked, dice.
3. Serve mash topped with chicken.""",
    },
    {
        "id": "shpinat_yaitsa",
        "name": "Яйця зі шпинатом",
        "name_en": "Eggs with spinach",
        "meal_type": "breakfast",
        "ingredients": {"шпинат": (80, "г"), "яйця": (2, "шт"), "сир": (40, "г"), "олія": (15, "г"), "сіль": (2, "г")},
        "recipe": """🌿 ЯЙЦЯ ЗІ ШПИНАТОМ

Інгредієнти:
• 80 г шпинату
• 2 яйця
• 40 г сиру, олія, сіль

Приготування:
1. Обсмажте шпинат на олії 1-2 хв.
2. Залийте збитими яйцями, посоліть.
3. Посипте сиром, готуйте під кришкою до схоплення.""",
        "recipe_en": """🌿 EGGS WITH SPINACH

Ingredients:
• 80 g spinach
• 2 eggs
• 40 g cheese, oil, salt

Steps:
1. Sauté spinach in oil for 1–2 minutes.
2. Pour in beaten eggs, season.
3. Add cheese, cover and cook until set.""",
    },
    {
        "id": "pasta_hriby",
        "name": "Паста з грибами у вершках",
        "name_en": "Creamy mushroom pasta",
        "meal_type": "lunch",
        "ingredients": {"макарони": (100, "г"), "гриби": (120, "г"), "цибуля": (30, "г"), "вершки": (80, "г"), "сіль": (2, "г")},
        "recipe": """🍄 ПАСТА З ГРИБАМИ

Інгредієнти:
• 100 г пасти
• 120 г грибів, цибуля
• 80 г вершків, сіль

Приготування:
1. Варіть пасту.
2. Підсмажте цибулю та гриби, влийте вершки, тушкуйте 5 хв.
3. Змішайте з пастою.""",
        "recipe_en": """🍄 CREAMY MUSHROOM PASTA

Ingredients:
• 100 g pasta
• 120 g mushrooms, onion
• 80 g cream, salt

Steps:
1. Boil pasta.
2. Sauté onion and mushrooms, add cream, simmer 5 minutes.
3. Toss with pasta.""",
    },
    {
        "id": "kabachkovi_oladi",
        "name": "Кабачкові оладки",
        "name_en": "Zucchini fritters",
        "meal_type": "lunch",
        "ingredients": {"кабачок": (200, "г"), "яйця": (1, "шт"), "борошно": (40, "г"), "сіль": (2, "г"), "олія": (30, "г")},
        "recipe": """🥒 КАБАЧКОВІ ОЛАДКИ

Інгредієнти:
• 200 г кабачка
• 1 яйце, 40 г борошна, сіль, олія

Приготування:
1. Натріть кабачок, відіжміть зайву воду.
2. Змішайте з яйцем і борошном.
3. Смажте оладки на олії з двох боків.""",
        "recipe_en": """🥒 ZUCCHINI FRITTERS

Ingredients:
• 200 g zucchini
• 1 egg, 40 g flour, salt, oil

Steps:
1. Grate zucchini, squeeze out excess liquid.
2. Mix with egg and flour.
3. Fry patties in oil on both sides.""",
    },
    {
        "id": "zapecheny_baklazhan",
        "name": "Запечений баклажан з сиром",
        "name_en": "Baked eggplant with cheese",
        "meal_type": "dinner",
        "ingredients": {"баклажан": (200, "г"), "помідори": (80, "г"), "сир": (50, "г"), "часник": (5, "г"), "олія": (15, "г"), "сіль": (2, "г")},
        "recipe": """🍆 ЗАПЕЧЕНИЙ БАКЛАЖАН

Інгредієнти:
• 1 баклажан, помідори, сир
• Часник, олія, сіль

Приготування:
1. Наріжте баклажан, підсоліть на 10 хв, промокніть.
2. Шари: баклажан, помідор, сир; збризніть олією.
3. Запікайте 20-25 хв при 190 °C.""",
        "recipe_en": """🍆 BAKED EGGPLANT WITH CHEESE

Ingredients:
• Eggplant, tomatoes, cheese
• Garlic, oil, salt

Steps:
1. Slice eggplant, salt 10 minutes, pat dry.
2. Layer eggplant, tomato, cheese; drizzle oil.
3. Bake 20–25 minutes at 190 °C.""",
    },
    {
        "id": "kvasolia_tush",
        "name": "Тушкована квасоля з м'ясом",
        "name_en": "Stewed beans with meat",
        "meal_type": "dinner",
        "ingredients": {"квасоля": (150, "г"), "м'ясо": (100, "г"), "морква": (40, "г"), "цибуля": (30, "г"), "помідори": (80, "г"), "сіль": (3, "г")},
        "recipe": """🫘 ТУШКОВАНА КВАСОЛЯ

Інгредієнти:
• 150 г квасолі (відвареної)
• 100 г м'яса, морква, цибуля, помідори, сіль

Приготування:
1. Обсмажте м'ясо з овочами.
2. Додайте квасолю та томати, тушкуйте 15-20 хв.""",
        "recipe_en": """🫘 STEWED BEANS WITH MEAT

Ingredients:
• 150 g cooked beans
• 100 g meat, carrot, onion, tomatoes, salt

Steps:
1. Brown meat with vegetables.
2. Add beans and tomatoes, simmer 15–20 minutes.""",
    },
    {
        "id": "kukurudza_kurka_salat",
        "name": "Салат з кукурудзою та куркою",
        "name_en": "Corn and chicken salad",
        "meal_type": "lunch",
        "ingredients": {"кукурудза": (100, "г"), "курка": (80, "г"), "огірки": (50, "г"), "йогурт": (60, "г"), "сіль": (2, "г")},
        "recipe": """🌽 САЛАТ З КУКУРУДЗОЮ ТА КУРКОЮ

Інгредієнти:
• 100 г кукурудзи
• 80 г вареної курки
• Огірок, йогурт, сіль

Приготування:
1. Наріжте курку та огірок.
2. Змішайте з кукурудзою, заправте йогуртом.""",
        "recipe_en": """🌽 CORN AND CHICKEN SALAD

Ingredients:
• 100 g corn
• 80 g cooked chicken
• Cucumber, yogurt, salt

Steps:
1. Dice chicken and cucumber.
2. Mix with corn, dress with yogurt.""",
    },
    {
        "id": "sup_hribnyi",
        "name": "Грибний суп з локшиною",
        "name_en": "Mushroom noodle soup",
        "meal_type": "dinner",
        "ingredients": {"гриби": (100, "г"), "картопля": (100, "г"), "морква": (40, "г"), "цибуля": (30, "г"), "лапша": (40, "г"), "сіль": (3, "г"), "зелень": (10, "г")},
        "recipe": """🍄 ГРИБНИЙ СУП

Інгредієнти:
• 100 г грибів
• Картопля, морква, цибуля
• Локшина, сіль, зелень

Приготування:
1. Варіть бульйон з овочами та грибами 15 хв.
2. Додайте локшину, варіть ще 5-7 хв.
3. Посипте зеленню.""",
        "recipe_en": """🍄 MUSHROOM NOODLE SOUP

Ingredients:
• 100 g mushrooms
• Potato, carrot, onion
• Noodles, salt, herbs

Steps:
1. Simmer broth with vegetables and mushrooms ~15 minutes.
2. Add noodles, cook 5–7 minutes more.
3. Garnish with herbs.""",
    },
    {
        "id": "ris_tunez",
        "name": "Рисовий салат з тунцем",
        "name_en": "Tuna rice bowl",
        "meal_type": "lunch",
        "ingredients": {"рис": (80, "г"), "тунець": (70, "г"), "огірки": (40, "г"), "лимон": (10, "г"), "соєвий соус": (15, "г"), "сіль": (1, "г")},
        "recipe": """🍚 РИС З ТУНЦЕМ

Інгредієнти:
• 80 г відвареного рису
• 70 г тунця, огірок
• Соєвий соус, лимон, сіль

Приготування:
1. Змішайте рис з тунцем і нарізаним огірком.
2. Заправте соєвим соусом і лимоном.""",
        "recipe_en": """🍚 TUNA RICE BOWL

Ingredients:
• 80 g cooked rice
• 70 g tuna, cucumber
• Soy sauce, lemon, salt

Steps:
1. Mix rice with tuna and diced cucumber.
2. Season with soy sauce and lemon.""",
    },
    {
        "id": "pechena_kartoplya",
        "name": "Запечена картопля з зеленню",
        "name_en": "Baked potatoes with herbs",
        "meal_type": "dinner",
        "ingredients": {"картопля": (400, "г"), "олія": (25, "г"), "сіль": (3, "г"), "зелень": (15, "г")},
        "recipe": """🥔 ЗАПЕЧЕНА КАРТОПЛЯ

Інгредієнти:
• 400 г картоплі
• Олія, сіль, зелень

Приготування:
1. Наріжте картоплю часточками.
2. Змішайте з олією та сіллю.
3. Запікайте 35-40 хв при 200 °C, посипте зеленню.""",
        "recipe_en": """🥔 BAKED POTATOES WITH HERBS

Ingredients:
• 400 g potatoes
• Oil, salt, herbs

Steps:
1. Cut potatoes into wedges.
2. Toss with oil and salt.
3. Bake 35–40 minutes at 200 °C; sprinkle herbs.""",
    },
    {
        "id": "ovocheve_ragu",
        "name": "Овочеве рагу",
        "name_en": "Vegetable stew",
        "meal_type": "dinner",
        "ingredients": {"картопля": (150, "г"), "морква": (50, "г"), "цибуля": (30, "г"), "помідори": (100, "г"), "кабачок": (100, "г"), "олія": (20, "г"), "сіль": (3, "г")},
        "recipe": """🍲 ОВОЧЕВЕ РАГУ

Інгредієнти:
• Картопля, морква, цибуля
• Помідори, кабачок, олія, сіль

Приготування:
1. Обсмажте цибулю та моркву.
2. Додайте решту овочів, тушкуйте під кришкою 20-25 хв.""",
        "recipe_en": """🍲 VEGETABLE STEW

Ingredients:
• Potato, carrot, onion
• Tomatoes, zucchini, oil, salt

Steps:
1. Sauté onion and carrot.
2. Add remaining vegetables, simmer covered 20–25 minutes.""",
    },
    {
        "id": "ribni_kotlety",
        "name": "Рибні котлети",
        "name_en": "Fish patties",
        "meal_type": "dinner",
        "ingredients": {"риба": (200, "г"), "картопля": (100, "г"), "цибуля": (40, "г"), "яйця": (1, "шт"), "борошно": (30, "г"), "сіль": (3, "г"), "олія": (25, "г")},
        "recipe": """🐠 РИБНІ КОТЛЕТИ

Інгредієнти:
• 200 г рибного філе
• 100 г вареної картоплі, цибуля, яйце, борошно, сіль, олія

Приготування:
1. Подрібніть рибу з картоплею та цибулею.
2. Додайте яйце, борошно, сіль; сформуйте котлети.
3. Обсмажте на олії.""",
        "recipe_en": """🐠 FISH PATTIES

Ingredients:
• 200 g fish fillet
• 100 g boiled potato, onion, egg, flour, salt, oil

Steps:
1. Mince fish with potato and onion.
2. Add egg, flour, salt; shape patties.
3. Pan-fry in oil.""",
    },
    {
        "id": "farshyrovanyi_perets",
        "name": "Фарширований перець",
        "name_en": "Stuffed bell peppers",
        "meal_type": "dinner",
        "ingredients": {"болгарський перець": (200, "г"), "рис": (60, "г"), "м'ясо": (100, "г"), "помідори": (80, "г"), "цибуля": (30, "г"), "сіль": (3, "г")},
        "recipe": """🫑 ФАРШИРОВАНИЙ ПЕРЕЦЬ

Інгредієнти:
• 2 болгарські перці
• Рис, м'ясо, помідори, цибуля, сіль

Приготування:
1. Змішайте сирий рис з фаршем, цибулею та томатами.
2. Наповніть перці, викладіть у форму з водою внизу.
3. Запікайте 45-50 хв при 180 °C.""",
        "recipe_en": """🫑 STUFFED BELL PEPPERS

Ingredients:
• 2 bell peppers
• Rice, meat, tomatoes, onion, salt

Steps:
1. Mix raw rice with minced meat, onion, and tomatoes.
2. Stuff peppers, place in a baking dish with a little water.
3. Bake 45–50 minutes at 180 °C.""",
    },
    {
        "id": "grechka_goroshok",
        "name": "Гречка з горошком",
        "name_en": "Buckwheat with peas",
        "meal_type": "lunch",
        "ingredients": {"гречка": (80, "г"), "горошок": (80, "г"), "морква": (40, "г"), "цибуля": (25, "г"), "олія": (15, "г"), "сіль": (2, "г")},
        "recipe": """🫛 ГРЕЧКА З ГОРОШКОМ

Інгредієнти:
• 80 г гречки
• 80 г горошку, морква, цибуля, олія, сіль

Приготування:
1. Підсмажте цибулю та моркву.
2. Додайте гречку, горошок і воду, варіть під кришкою 15-18 хв.""",
        "recipe_en": """🫛 BUCKWHEAT WITH PEAS

Ingredients:
• 80 g buckwheat
• 80 g peas, carrot, onion, oil, salt

Steps:
1. Sauté onion and carrot.
2. Add buckwheat, peas, and water; simmer covered 15–18 minutes.""",
    },
    {
        "id": "bliny_banan",
        "name": "Млинці з бананом",
        "name_en": "Banana pancakes",
        "meal_type": "breakfast",
        "ingredients": {"борошно": (80, "г"), "молоко": (150, "г"), "яйця": (1, "шт"), "банан": (1, "шт"), "цукор": (20, "г"), "масло": (15, "г")},
        "recipe": """🥞 МЛИНЦІ З БАНАНОМ

Інгредієнти:
• 80 г борошна, 150 мл молока
• 1 яйце, 1 банан, цукор, масло

Приготування:
1. Розімніть банан виделкою, змішайте з молоком та яйцем.
2. Додайте борошно і цукор.
3. Смажте млинці на маслі з двох боків.""",
        "recipe_en": """🥞 BANANA PANCAKES

Ingredients:
• 80 g flour, 150 ml milk
• 1 egg, 1 banana, sugar, butter

Steps:
1. Mash banana, mix with milk and egg.
2. Add flour and sugar.
3. Fry pancakes in butter on both sides.""",
    },
    {
        "id": "shokoladna_vivsianka",
        "name": "Шоколадна вівсянка",
        "name_en": "Chocolate oatmeal",
        "meal_type": "breakfast",
        "ingredients": {"вівсянка": (50, "г"), "молоко": (180, "г"), "какао": (10, "г"), "цукор": (15, "г"), "банан": (1, "шт")},
        "recipe": """🍫 ШОКОЛАДНА ВІВСЯНКА

Інгредієнти:
• 50 г вівсянки
• 180 мл молока, какао, цукор, банан

Приготування:
1. Доведіть молоко з какао та цукром до кипіння.
2. Додайте вівсянку, варіть 4-5 хв.
3. Подавайте з нарізаним бананом.""",
        "recipe_en": """🍫 CHOCOLATE OATMEAL

Ingredients:
• 50 g oats
• 180 ml milk, cocoa, sugar, banana

Steps:
1. Heat milk with cocoa and sugar to a boil.
2. Add oats, cook 4–5 minutes.
3. Top with sliced banana.""",
    },
    {
        "id": "yabluchny_crumble",
        "name": "Яблучний крамбл",
        "name_en": "Apple crumble",
        "meal_type": "dessert",
        "ingredients": {"яблука": (200, "г"), "борошно": (60, "г"), "масло": (50, "г"), "цукор": (40, "г")},
        "recipe": """🍎 ЯБЛУЧНИЙ КРАМБЛ

Інгредієнти:
• 200 г яблук
• 60 г борошна, 50 г масла, 40 г цукру

Приготування:
1. Наріжте яблука, викладіть у форму.
2. Перетріть масло з борошном і цукром у крихту.
3. Посипте яблука, запікайте 30 хв при 180 °C.""",
        "recipe_en": """🍎 APPLE CRUMBLE

Ingredients:
• 200 g apples
• 60 g flour, 50 g butter, 40 g sugar

Steps:
1. Slice apples into a baking dish.
2. Rub butter with flour and sugar into crumbs.
3. Sprinkle over apples, bake 30 minutes at 180 °C.""",
    },
    {
        "id": "yogurt_parfe",
        "name": "Йогуртове парфе з ягодами",
        "name_en": "Berry yogurt parfait",
        "meal_type": "breakfast",
        "ingredients": {"йогурт": (150, "г"), "ягоди": (80, "г"), "цукор": (10, "г"), "мед": (15, "г")},
        "recipe": """🫐 ЙОГУРТОВЕ ПАРФЕ

Інгредієнти:
• 150 г йогурту
• 80 г ягід, цукор, мед

Приготування:
1. Змішайте йогурт з цукром.
2. Шарами: йогурт, ягоди, мед — у склянці.
3. Подавайте одразу.""",
        "recipe_en": """🫐 BERRY YOGURT PARFAIT

Ingredients:
• 150 g yogurt
• 80 g berries, sugar, honey

Steps:
1. Mix yogurt with sugar.
2. Layer yogurt, berries, and honey in a glass.
3. Serve immediately.""",
    },
    {
        "id": "french_toast",
        "name": "Французькі тости",
        "name_en": "French toast",
        "meal_type": "breakfast",
        "ingredients": {"хліб": (3, "шт"), "молоко": (100, "г"), "яйця": (2, "шт"), "цукор": (25, "г"), "масло": (25, "г")},
        "recipe": """🍞 ФРАНЦУЗЬКІ ТОСТИ

Інгредієнти:
• 3 скибочки хліба
• 100 мл молока, 2 яйця, цукор, масло

Приготування:
1. Збийте молоко з яйцями та цукром.
2. Змочіть хліб, обсмажте на маслі до рум'янця.
3. Подавайте теплими.""",
        "recipe_en": """🍞 FRENCH TOAST

Ingredients:
• 3 bread slices
• 100 ml milk, 2 eggs, sugar, butter

Steps:
1. Whisk milk with eggs and sugar.
2. Dip bread, fry in butter until golden.
3. Serve warm.""",
    },
]


def normalize_ingredient(name: str) -> str | None:
    """Нормалізує назву інгредієнта за допомогою аліасів."""
    name_lower = name.lower().strip()
    for standard, aliases in INGREDIENT_ALIASES.items():
        if name_lower in aliases or any(a in name_lower for a in aliases):
            return standard
    return name_lower if name_lower else None


# Продукти, які зазвичай є в кожній кухні (не потрібно вказувати)
PANTRY = {"сіль", "перець", "олія", "масло"}
MIN_MATCHED_INGREDIENTS = 3


def recipe_title(recipe: dict, lang: str) -> str:
    """Localized dish title for menus (recipe text stays as stored)."""
    if lang == "en":
        return recipe.get("name_en") or recipe["name"]
    return recipe["name"]


def ingredient_keys_formatted(lang: str = "uk") -> str:
    """Список інгредієнтів для бота (мова відображення)."""
    return ingredient_catalog_formatted(lang)


def get_recipes_by_ingredients(user_products: dict) -> list:
    """
    user_products: {назва: (кількість, одиниця)} — кількості ігноруються для відбору;
    важлива лише наявність нормалізованої назви інгредієнта.
    """
    available = {}
    for name, (qty, unit) in user_products.items():
        norm = normalize_ingredient(name) or name.lower().strip()
        if not norm:
            continue
        if norm in available:
            old_q, old_u = available[norm]
            available[norm] = (old_q + qty, old_u)
        else:
            available[norm] = (qty, unit)

    result = []
    for r in RECIPES:
        matched_main = 0
        for ing, (min_qty, min_unit) in r["ingredients"].items():
            norm_ing = normalize_ingredient(ing) or ing.lower()
            if norm_ing in PANTRY:
                continue
            if norm_ing in available:
                matched_main += 1
        if matched_main >= MIN_MATCHED_INGREDIENTS:
            result.append(r)
    return result


def generate_menu_variants(recipes: list, count: int = 3) -> list[list[dict]]:
    """
    Генерує count варіантів збалансованого меню на день.
    Кожне меню: сніданок, обід, вечеря.
    """
    import random

    breakfasts = [r for r in recipes if r["meal_type"] == "breakfast"]
    lunches = [r for r in recipes if r["meal_type"] == "lunch"]
    dinners = [r for r in recipes if r["meal_type"] in ("dinner", "dessert")]

    fallback = recipes[0] if recipes else None
    b_list = breakfasts if breakfasts else ([fallback] if fallback else [])
    l_list = lunches if lunches else ([fallback] if fallback else [])
    d_list = dinners if dinners else ([fallback] if fallback else [])

    variants = []
    used_combos = set()

    for _ in range(count * 2):
        if len(variants) >= count:
            break
        b = random.choice(b_list)
        l = random.choice(l_list)
        d = random.choice(d_list)
        combo = (b["id"], l["id"], d["id"])
        if combo not in used_combos:
            used_combos.add(combo)
            variants.append([b, l, d])

    return variants[:count]
