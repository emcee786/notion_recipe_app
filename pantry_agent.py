import os
from openai import OpenAI
import json


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def simplify_ingredients(ingredient_list):
    prompt = f"""
    You're a kitchen assistant.

    Take the raw list of recipe ingredients below and clean it up.

    Your job is to return a **clean, deduplicated** list of simplified ingredient names.

    Rules to follow:
    - Remove all **quantities, units, brands, and prep instructions**
    - **Remove anything in parentheses**
    - Keep key descriptors that define the ingredient (e.g. "brown sugar", "vanilla extract", "self-raising flour")
    - Merge duplicates and similar things into one consistent name (e.g. "caster sugar", "granulated sugar" → "Sugar")

    Return the result as a **valid Python list of strings** like:
    [
    "Flour",
    "Sugar",
    "Vanilla Extract"
    ]

    Ingredients:
    {ingredient_list}

    Output:
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    result = response.choices[0].message.content.strip()

    try:
        parsed = eval(result) if result.startswith("[") else []
    except Exception:
        print("⚠️ Could not parse LLM response:", result)
        parsed = []

    return parsed




def add_pantry_items_to_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        recipe = json.load(f)

    ingredients = recipe.get("ingredients", [])
    pantry_items = simplify_ingredients(ingredients)
    print(ingredients)

    # Deduplicate case-insensitively
    seen = set()
    unique_items = []
    for item in pantry_items:
        item_clean = item.strip()
        if item_clean.lower() not in seen:
            unique_items.append(item_clean)
            seen.add(item_clean.lower())

    recipe["pantry_items"] = unique_items

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(recipe, f, indent=4, ensure_ascii=False)

    print(f"✅ Pantry items added to '{file_path}'")
    print("\n🧂 Pantry Items:")
    for item in unique_items:
        print(f"- {item}")


if __name__ == "__main__":
    add_pantry_items_to_json("Orange_and_Poppy_Seed_Cake.json") 