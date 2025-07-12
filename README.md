📋 Overview

This project scrapes recipes from supported websites and saves them as JSON files. It also includes:

    ✅ Custom scrapers for sites not supported by recipe-scrapers

    ✅ A Pantry Agent that deduplicates and simplifies ingredient lists

    ✅ Automatic Notion upload of recipes and their pantry items

    🔜 Planned meal planning and pantry tracking features

✅ Recipe Scraping

    Uses recipe-scrapers to extract structured recipe data from supported websites.

    Custom scrapers inherit from the AbstractScraper class to support unsupported sites like chelsea.co.nz.

✅ Pantry Agent

    Simplifies ingredients to pantry items (e.g., "1 cup shredded cheddar" → "Cheese").

    Removes units, preparation instructions, and duplicates.

    Uses OpenAI for semantic simplification.

✅ Notion Integration

    Uploads recipe data to a Notion database.

    Links pantry items to recipes.

    Adds new pantry items if not already in the database.

🔜 Hope to add

    🥗 Meal planning 

    🧂 Pantry tracking

    📦 Integration with supermarket APIs