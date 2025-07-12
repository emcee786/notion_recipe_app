import os
from openai import OpenAI
import json


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
CATEGORIES = ["Dairy", "Produce", "Meat", "Seafood", "Frozen", "Herbs & Spices", "Pantry", "Condiments", "Other"]


def simplify_ingredients(ingredient_list):
    prompt = """
You are a kitchen assistant.

Your job is to extract a **clean, deduplicated** list of pantry ingredients from raw recipe inputs.

You must follow these rules carefully:

- Remove all **quantities, units, brands, preparation instructions, and content in parentheses**
- **Keep important descriptors** that materially change the item identity (e.g., "brown sugar", "vanilla ice cream", "self-raising flour")
- **Simplify varieties or brand-specific words** that don’t affect the ingredient’s nature 
  (e.g., "Gala apples" → "Apples", "Butter puff pastry" → "Puff Pastry")
- **Merge functionally identical items** into a **single canonical form** — 
  (e.g., "Ground Cinnamon", "Cinnamon Powder" → "Cinnamon"; "Cheddar Cheese", "Shredded Cheese" → "Cheese")

Return a valid **Python list of strings** like:
[
  "Butter",
  "Brown Sugar"
]

**Avoid duplicates by normalizing similar items to a single entry.**

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
    add_pantry_items_to_json("Super_Moist_Chocolate_Cupcakes.json") 