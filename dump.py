import os
import requests
from urllib.parse import urlparse

def scrape_recipe_to_txt(url):
    """
    Scrapes the content from a recipe URL and dumps it to a text file in the 'web_data' folder.
    The text file is named after the URL's hostname.
    """
    # Parse hostname
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    if not hostname:
        raise ValueError("Invalid URL: Hostname could not be determined.")

    # Create folder if it doesn't exist
    folder = "web_data"
    os.makedirs(folder, exist_ok=True)

    # Fetch content
    response = requests.get(url)
    response.raise_for_status()
    content = response.text

    # Write to file
    file_path = os.path.join(folder, f"{hostname}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Recipe dumped to {file_path}")

def main():
    # Example usage
    url = "https://www.chelsea.co.nz/recipes/browse-recipes/banana-bread"
    scrape_recipe_to_txt(url)

if __name__ == "__main__":
    main()
