from recipe_scrapers import scrape_me
from custom_scrapers import KiwiCountryGirlScraper, ChelseaSugarScraper, SweetestMenuScraper,  WoolworthsScraper
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


if __name__ == "__main__":
    url = "https://www.woolworths.co.nz/recipes/lunch/3131/wintery-green-salad-with-green-goddess-dressing"  
    download_recipe(WoolworthsScraper, url)



