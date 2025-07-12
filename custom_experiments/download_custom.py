import json
import re
import requests
from bs4 import BeautifulSoup
from custom_experiments.custom_scraper import KiwiCountryGirl  # your custom scraper

def sanitize_filename(title):
    return re.sub(r"[^\w\-_. ]", "", title).replace(" ", "_")

def download_recipe(url):
    # Get HTML content
    html = requests.get(url).text

    # Pass URL and HTML to your custom scraper (not soup!)
    scraper = KiwiCountryGirl(url, html)

    # Extract data
    data = {
        "title": scraper.title(),
        "total_time": scraper.total_time(),
        "yields": scraper.yields(),
        "ingredients": scraper.ingredients(),
        "instructions": scraper.instructions(),
        "image": scraper.image(),
        "author": scraper.author(),
        "host": scraper.host(),
        "canonical_url": scraper.canonical_url()
    }

    # Save to file
    filename = sanitize_filename(data["title"]) + ".json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Recipe saved to {filename}")

if __name__ == "__main__":
    download_recipe("https://www.thekiwicountrygirl.com/boysenberry-white-chocolate-no-bake-cheesecake/")
