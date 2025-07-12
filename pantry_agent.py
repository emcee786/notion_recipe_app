import os
from openai import OpenAI
import json
import csv

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
CATEGORIES = ["Dairy", "Produce", "Meat", "Seafood", "Frozen", "Herbs & Spices", "Pantry", "Condiments", "Other"]
CSV_FILE = "pantry_master.csv"

def simplify_ingredients(ingredient_list):
    prompt = f"""
You are a kitchen assistant.

Your job is to extract a **clean, deduplicated** list of pantry ingredients from raw recipe inputs.

You must follow these rules carefully:

- Remove all **quantities, units, brands, preparation instructions, and content in parentheses**
- **Keep important descriptors** that materially change the item identity (e.g., "brown sugar", "vanilla ice cream", "self-raising flour")
- **Simplify varieties or brand-specific words** that don’t affect the ingredient’s nature 
  (e.g., "Gala apples" → "Apples", "Butter puff pastry" → "Puff Pastry")
- **Merge functionally identical items** into a **single canonical form** — 
  (e.g., "Ground Cinnamon", "Cinnamon Powder" → "Cinnamon"; "Cheddar Cheese", "Shredded Cheese" → "Cheese")
- Assign one of the following **categories** to each item:
  {", ".join(CATEGORIES)}

Return a valid **Python list of dictionaries** like:
[
  {{"item": "Butter", "category": "Dairy"}},
  {{"item": "Brown Sugar", "category": "Baking"}}
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

def load_existing_csv_items():
    existing_items = set()
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_items.add(row["item"].lower())
    return existing_items


def update_csv(pantry_list):
    existing_items = load_existing_csv_items()
    added_items = set(existing_items)  # So we can update during loop

    new_rows = []
    for row in pantry_list:
        item_lower = row["item"].strip().lower()
        if item_lower not in added_items:
            new_rows.append(row)
            added_items.add(item_lower)  # Track this as added

    if new_rows:
        file_exists = os.path.exists(CSV_FILE)
        with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["item", "category"])
            if not file_exists:
                writer.writeheader()
            writer.writerows(new_rows)


def add_pantry_items_to_json(file_path):
    # Load the recipe JSON
    with open(file_path, "r", encoding="utf-8") as f:
        recipe = json.load(f)

    # Extract and simplify ingredients
    ingredients = recipe.get("ingredients", [])
    pantry_structured = simplify_ingredients(ingredients)

    # Deduplicate item names case-insensitively
    seen_items = set()
    unique_items = []
    for row in pantry_structured:
        item_lower = row["item"].strip().lower()
        if item_lower not in seen_items:
            unique_items.append(row["item"].strip())
            seen_items.add(item_lower)

    # Save just the unique item names to JSON
    recipe["pantry_items"] = unique_items

    # Save updated JSON
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(recipe, f, indent=4, ensure_ascii=False)

    # Update the master pantry CSV
    update_csv(pantry_structured)

    # Print summary
    print(f"✅ Pantry items added to '{file_path}' and updated in CSV.")
    print("\n🧂 Pantry Items:")
    for row in unique_items:
        print(f"- {row}")


if __name__ == "__main__":
    add_pantry_items_to_json("Boysenberry__White_Chocolate_No_Bake_Cheesecake.json") 