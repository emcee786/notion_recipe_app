from recipe_scrapers import scrape_me
from archive.custom_scrapers import CustomRecipeScraper
from custom_scrapers.kiwi_country_girl import KiwiCountryGirlScraper
from custom_scrapers.chelsea_sugar import ChelseaSugarScraper
import json
import re

def slugify_title(title: str) -> str:
    """Create sa safe filename from a recipe title."""
    return re.sub(r"[^\w\-_. ]", "", title).strip().replace(" ", "_")

def download_recipe(scraper_class, url):
    """Download and save recipe JSON using the given scraper class and URL."""
    scraper = scraper_class(url)

    # If the scraper needs to fetch content manually (like a custom one)
    if hasattr(scraper, "fetch") and callable(getattr(scraper, "fetch")):
        scraper.fetch()

    recipe_data = {
        "title": scraper.title(),
        "total_time": scraper.total_time(),
        "yields": scraper.yields(),
        "ingredients": scraper.ingredients(),
        "instructions": scraper.instructions(),
        "image": scraper.image(),
        "host": scraper.host(),
        "author": scraper.author(),
        "language": scraper.language(),
        "canonical_url": scraper.canonical_url(),
    }

    output_filename = f"{slugify_title(recipe_data['title'])}.json"

    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(recipe_data, f, ensure_ascii=False, indent=4)

    print(f"✅ Recipe saved to '{output_filename}'")


# def supported_recipe_download(url: str):
#     # Scrape the recipe
#     scraper = scrape_me(url)
#     # Convert the recipe to a dictionary
#     recipe_data = {
#         "title": scraper.title(),
#         "total_time": scraper.total_time(),
#         "yields": scraper.yields(),
#         "ingredients": scraper.ingredients(),
#         "instructions": scraper.instructions(),
#         "image": scraper.image(),
#         "host": scraper.host(),
#         "author": scraper.author(),
#         "language": scraper.language(),
#         "canonical_url": scraper.canonical_url()
#     }

#     output_filename = f"{slugify_title(recipe_data['title'])}.json"

#     # Write the dictionary to a JSON file
#     with open(output_filename, "w", encoding="utf-8") as f:
#         json.dump(recipe_data, f, ensure_ascii=False, indent=4)



# def custom_recipe_download(url):
#     scraper = CustomRecipeScraper(url)
#     scraper.fetch()

#     recipe_data = {
#         "title": scraper.title(),
#         "total_time": scraper.total_time(),
#         "yields": scraper.yields(),
#         "ingredients": scraper.ingredients(),
#         "instructions": scraper.instructions(),
#         "image": scraper.image(),
#         "host": scraper.host(),
#         "author": scraper.author(),
#         "language": scraper.language(),
#         "canonical_url": scraper.canonical_url(),

#         # Notion-compatible fields
#         "pantry_items": scraper.ingredients(),
#         "category": []
#     }

#     output_filename = f"{slugify_title(recipe_data['title'])}.json"

#     # Save JSON
#     with open(output_filename, "w", encoding="utf-8") as f:
#         json.dump(recipe_data, f, ensure_ascii=False, indent=4)

#     print(f"✅ Recipe saved to '{output_filename}'")

if __name__ == "__main__":
    url = "https://www.chelsea.co.nz/recipes/browse-recipes/super-moist-chocolate-cupcakes"  
    download_recipe(ChelseaSugarScraper, url)



