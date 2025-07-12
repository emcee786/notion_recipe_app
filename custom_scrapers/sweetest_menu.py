import requests
from recipe_scrapers._abstract import AbstractScraper


class SweetestMenuScraper(AbstractScraper):
    @classmethod
    def host(cls):
        return "sweetestmenu.com"

    def __init__(self, url, **kwargs):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html = response.text

        super().__init__(html, url)

    def title(self):
        return self.soup.find("h1").get_text(strip=True)

    def total_time(self):
        try:
            return self.soup.select_one("span.tasty-recipes-total-time").get_text(strip=True)
        except AttributeError:
            return None

    def yields(self):
        serving_size = self.soup.select_one(".tasty-recipes-serving-size")
        return serving_size.get_text(strip=True) if serving_size else None

    def image(self):
        meta_img = self.soup.find("meta", property="og:image")
        return meta_img["content"] if meta_img else None

    def ingredients(self):
        container = self.soup.select_one(".tasty-recipes-ingredients")
        return [li.get_text(" ", strip=True) for li in container.find_all("li")] if container else []

    def instructions(self):
        steps = self.soup.select(".tasty-recipes-instructions ol li")
        return "\n".join([step.get_text(strip=True) for step in steps])

    def author(self):
        author = self.soup.select_one(".tasty-recipes-author-name")
        return author.get_text(strip=True) if author else "Unknown"

    def canonical_url(self):
        tag = self.soup.find("link", rel="canonical")
        return tag["href"] if tag else self.url

    def language(self):
        html = self.soup.find("html")
        return html.get("lang", "en") if html else "en"