import os
import requests
from urllib.parse import urlparse

"""
🧪 Recipe HTML Dumper – Just a helper script.

This script is mainly for dumping the raw HTML content of a recipe page 
to a local text file. It's part of the workflow for building custom scrapers 
for sites that aren't supported by recipe-scrapers.

It grabs the HTML from a given URL, saves it under `web_data/` using the 
domain name as the filename, and that's it.

Super handy when I'm trying to reverse engineer the structure of a recipe page 
(e.g. what tags they're using for ingredients/instructions) so I can write a 
custom AbstractScraper subclass for that site.
"""


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    )
}

def scrape_recipe_to_txt(url):
    """
    Scrapes the raw HTML from a recipe URL and saves it to a text file 
    in the 'web_data' folder, named after the domain.
    """
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    if not hostname:
        raise ValueError("Invalid URL: Hostname could not be determined.")

    os.makedirs("web_data", exist_ok=True)

    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    content = response.text

    file_path = os.path.join("web_data", f"{hostname}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Recipe HTML dumped to '{file_path}'")
  
  
if __name__ == "__main__":
    url = "https://www.woolworths.co.nz/recipes/lunch/3131/wintery-green-salad-with-green-goddess-dressing"
    scrape_recipe_to_txt(url)