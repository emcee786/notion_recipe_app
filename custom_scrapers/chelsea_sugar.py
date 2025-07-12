from recipe_scrapers._abstract import AbstractScraper
import json


import json
import requests


class ChelseaSugarScraper(AbstractScraper):
    @classmethod
    def host(cls):
        return "chelsea.co.nz"

    def __init__(self, url, **kwargs):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html = response.text

        super().__init__(html, url)
        self.data = self._extract_json_ld()

    def _extract_json_ld(self):
        for script in self.soup.find_all("script", type="application/ld+json"):
            try:
                content = json.loads(script.string.strip())

                if isinstance(content, list):
                    for entry in content:
                        if entry.get("@type") == "Recipe":
                            return entry
                elif content.get("@type") == "Recipe":
                    return content
            except (json.JSONDecodeError, AttributeError):
                continue

        raise ValueError("No JSON-LD Recipe data found")

    def title(self):
        return self.data.get("name")

    def total_time(self):
        prep = self.data.get("prepTime", "")
        cook = self.data.get("cookTime", "")
        return f"{prep} + {cook}".strip(" +") or None

    def yields(self):
        return self.data.get("recipeYield")

    def image(self):
        return self.data.get("image")

    def ingredients(self):
        return self.data.get("recipeIngredient", [])

    def instructions(self):
        instructions = self.data.get("recipeInstructions")
        if isinstance(instructions, str):
            return instructions
        elif isinstance(instructions, list):
            return "\n".join(
                step.get("text", "") if isinstance(step, dict) else str(step)
                for step in instructions
            )
        return ""

    def author(self):
        author = self.data.get("author")
        if isinstance(author, dict):
            return author.get("name")
        return "Unknown"

    def canonical_url(self):
        tag = self.soup.find("link", rel="canonical")
        return tag["href"] if tag else self.url

    def language(self):
        html = self.soup.find("html")
        return html.get("lang", "en") if html else "en"
