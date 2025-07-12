import json
from notion_client import Client
import os
from dotenv import load_dotenv

load_dotenv()  

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
RECIPE_DATABASE_ID = os.getenv("RECIPE_DATABASE_ID")
PANTRY_DATABASE_ID = os.getenv("PANTRY_DATABASE_ID")

notion = Client(auth=NOTION_TOKEN)


def get_or_create_pantry_items(pantry_items):
    """
    Ensure each pantry item exists in the Pantry DB and return their Notion page IDs.
    """
    page_ids = []

    for item in pantry_items:
        # 1. Search for the pantry item in Pantry
        response = notion.databases.query(
            database_id=PANTRY_DATABASE_ID,
            filter={
                "property": "Item",
                "rich_text": {
                    "equals": item
                }
            }
        )

        if response["results"]:
            # Item exists
            pantry_page_id = response["results"][0]["id"]
        else:
            # 2. Create it if it doesn't exist
            new_pantry_page = notion.pages.create(
                parent={"database_id": PANTRY_DATABASE_ID},
                icon={
                "type": "emoji",
                "emoji": "🥬"  # Pantry icon
            },
                properties={
                    "Item": {
                        "title": [{"text": {"content": item}}]
                    },
                    "Shopping List": {
                        "checkbox": False
                    }
                }
            )
            pantry_page_id = new_pantry_page["id"]

        page_ids.append({"id": pantry_page_id})

    return page_ids

def add_recipe_to_notion(recipe):
    pantry_ids = get_or_create_pantry_items(recipe.get("pantry_items", []))

    page = notion.pages.create(
        parent={"database_id": RECIPE_DATABASE_ID},
        icon={
        "type": "emoji",
        "emoji": "🍽️"
        },
        cover={
            "type": "external",
            "external": {"url": recipe["image"]}
        },
        properties={
            "Title": {
                "title": [{"text": {"content": recipe["title"]}}]
            },
            "Total Time": {
                "rich_text": [{"text": {"content": recipe["total_time"]}}]
            },
            "Yields": {
                "rich_text": [{"text": {"content": recipe["yields"]}}]
            },
            "Author": {
                "rich_text": [{"text": {"content": recipe["author"]}}]
            },
            "Host": {
                "rich_text": [{"text": {"content": recipe["host"]}}]
            },
            "URL": {
                "url": recipe["canonical_url"]
            },
            "Image": {
                "url": recipe["image"]
            },
            "Pantry": {
                "relation": pantry_ids  # ← Now using Notion page IDs
            },
            "Category": {
                "multi_select": [{"name": item} for item in recipe.get("category", [])]
            }
        },
        children = [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "Ingredients"}}]
                }
            },
            *[
                {
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": ingredient}}]
                    }
                }
                for ingredient in recipe["ingredients"]
            ],
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "Instructions"}}]
                }
            },
            *[
                {
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": step.strip()}}]
                    }
                }
                for step in recipe["instructions"].split("\n") if step.strip()
            ]
        ])
    print(f"✅ Recipe '{recipe['title']}' added with {len(pantry_ids)} linked pantry items.")

if __name__ == "__main__":
    # Load the recipe JSON
    with open("Super_Moist_Chocolate_Cupcakes.json", "r", encoding="utf-8") as f:
        recipe = json.load(f)
    
    add_recipe_to_notion(recipe)
