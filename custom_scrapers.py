import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class CustomRecipeScraper:
    """KiwiCountryGirl """
    def __init__(self, url: str):
        self.url = url
        self.soup = None

    def fetch(self):
        """Fetch the page content and parse with BeautifulSoup"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(self.url, headers=headers)
        response.raise_for_status()
        self.soup = BeautifulSoup(response.content, "html.parser")

    def _select_text(self, selector: str):
        """Helper to get text from a single element"""
        tag = self.soup.select_one(selector)
        return tag.get_text(strip=True) if tag else None

    def title(self):
        return self._select_text("h1.entry-title")

    def total_time(self):
        # Combine hours and minutes from different spans
        hours = self._select_text(".wprm-recipe-total_time-hours")
        minutes = self._select_text(".wprm-recipe-total_time-minutes")
        time_str = ""
        if hours:
            time_str += f"{hours} hours "
        if minutes:
            time_str += f"{minutes} minutes"
        return time_str.strip() or "Not found"

    def yields(self):
        return self._select_text(".wprm-recipe-servings") or "Not found"

    def author(self):
        return self._select_text(".wprm-recipe-author") or "Unknown"

    def ingredients(self):
        ingredients = []
        for li in self.soup.select("li.wprm-recipe-ingredient"):
            parts = [span.get_text(strip=True) for span in li.select(
                ".wprm-recipe-ingredient-amount, "
                ".wprm-recipe-ingredient-unit, "
                ".wprm-recipe-ingredient-name, "
                ".wprm-recipe-ingredient-notes"
            )]
            ingredient = " ".join(filter(None, parts))
            ingredients.append(ingredient)
        return ingredients

    def instructions(self):
        return "\n".join(
            step.get_text(strip=True)
            for step in self.soup.select("div.wprm-recipe-instruction-text")
        )

    def image(self):
        tag = self.soup.find("meta", property="og:image")
        return tag["content"] if tag and tag.get("content") else None

    def host(self):
        return urlparse(self.url).hostname

    def language(self):
        return self.soup.html.get("lang", "en")

    def canonical_url(self):
        tag = self.soup.find("link", rel="canonical")
        return tag["href"] if tag else self.url

    def to_dict(self):
        return {
            "title": self.title(),
            "total_time": self.total_time(),
            "yields": self.yields(),
            "ingredients": self.ingredients(),
            "instructions": self.instructions(),
            "image": self.image(),
            "host": self.host(),
            "author": self.author(),
            "language": self.language(),
            "canonical_url": self.canonical_url(),
        }


if __name__ == "__main__":
    url = "https://www.thekiwicountrygirl.com/boysenberry-white-chocolate-no-bake-cheesecake/"
    scraper = CustomRecipeScraper(url)
    scraper.fetch()
    recipe = scraper.to_dict()

    for key, value in recipe.items():
        print(f"{key.upper()}:\n{value}\n")
