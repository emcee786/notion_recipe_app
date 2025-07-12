import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from recipe_scrapers._abstract import AbstractScraper


class KiwiCountryGirlScraper(AbstractScraper):
    @classmethod
    def host(cls):
        return "thekiwicountrygirl.com" 

    def __init__(self, url, **kwargs):
        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        response.raise_for_status()
        html = response.text

        super().__init__(html, url)

    def _select_text(self, selector: str):
        tag = self.soup.select_one(selector)
        return tag.get_text(strip=True) if tag else None

    def title(self):
        return self._select_text("h1.entry-title")

    def total_time(self):
        hours = self._select_text(".wprm-recipe-total_time-hours")
        minutes = self._select_text(".wprm-recipe-total_time-minutes")
        time_str = ""
        if hours:
            time_str += f"{hours} hours "
        if minutes:
            time_str += f"{minutes} minutes"
        return time_str.strip() or None

    def yields(self):
        return self._select_text(".wprm-recipe-servings")

    def author(self):
        return self._select_text(".wprm-recipe-author")

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

    def language(self):
        return self.soup.html.get("lang", "en")

    def canonical_url(self):
        tag = self.soup.find("link", rel="canonical")
        return tag["href"] if tag else self.url