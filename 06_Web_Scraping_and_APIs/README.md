# Web Scraping & APIs

This module covers practical web scraping and API interaction techniques for data science and machine learning pipelines.

---

## 📁 Directory Structure

- [`01_API_basics.ipynb`](file:///c:/Users/Manis/OneDrive/vs%20COdE%20Python/Data-Science-Journey/06_Web_Scraping_and_APIs/01_API_basics.ipynb): Basics of REST APIs, HTTP methods, headers, and parsing JSON.
- [`02_web_scraping_BeautifulSoup.ipynb`](file:///c:/Users/Manis/OneDrive/vs%20COdE%20Python/Data-Science-Journey/06_Web_Scraping_and_APIs/02_web_scraping_BeautifulSoup.ipynb): Foundations of HTML parsing with BeautifulSoup.
- [`03_imdb_web_scraping_complete.ipynb`](file:///c:/Users/Manis/OneDrive/vs%20COdE%20Python/Data-Science-Journey/06_Web_Scraping_and_APIs/03_imdb_web_scraping_complete.ipynb): Comprehensive guide to scraping modern dynamic sites (Next.js, JSON-LD, anti-bot handling) and exploratory data analysis.
- [`imdb_scraper/`](file:///c:/Users/Manis/OneDrive/vs%20COdE%20Python/Data-Science-Journey/06_Web_Scraping_and_APIs/imdb_scraper): Complete, production-grade IMDb scraper package.
- [`demo_imdb_scraper.py`](file:///c:/Users/Manis/OneDrive/vs%20COdE%20Python/Data-Science-Journey/06_Web_Scraping_and_APIs/demo_imdb_scraper.py): Executable script demonstrating all scraper functionalities.

---

## 🎬 Complete IMDb Scraper Package

A full-featured scraper capable of handling modern Next.js client-side hydration, AWS WAF challenges, and structured JSON-LD schemas.

### 🌟 Features
1. **Instant Search**: Sub-second search for movies, shows, and people using IMDb's Suggestion API.
2. **Top Charts**: Scrapes Top 250 Movies, Top 250 TV Shows, and Most Popular (MovieMeter/TVMeter).
3. **Deep Metadata**: Retrieves Title, Release Date, Rating, Vote Count, Metascore, Runtime, Certificate, Genres, Directors, Writers, Cast, Box Office (Budget & Worldwide Gross), Plot, Poster, and Trailer URLs.
4. **Anti-Detection**: Built-in stealth browser engine bypassing AWS WAF / Cloudflare challenges.
5. **Data Export**: Directly converts to Pandas DataFrame, CSV, or JSON.

---

### 💻 Python Usage

```python
from imdb_scraper import IMDbScraper

with IMDbScraper(headless=True) as scraper:
    # 1. Instant Search
    results = scraper.search("Interstellar", limit=5)
    print(results)

    # 2. Scrape Top 250 Movies
    top_movies = scraper.get_top_250_movies(limit=50)
    df = scraper.to_dataframe(top_movies)
    print(df.head())

    # 3. Deep Movie Details (Budget, Gross, Cast, Ratings)
    details = scraper.get_movie_details("tt0111161")  # The Shawshank Redemption
    print(details)

    # 4. Save to files
    scraper.save_to_csv(top_movies, "top_movies.csv")
    scraper.save_to_json(details, "shawshank.json")
```

---

### ⌨️ CLI Usage

You can also run scraping tasks directly from the command line:

```bash
# Instant Search
python -m imdb_scraper.cli search "The Dark Knight"

# Top 50 Movies to CSV
python -m imdb_scraper.cli top-movies --limit 50 --output top50_movies.csv

# Top 25 TV Shows to JSON
python -m imdb_scraper.cli top-tv --limit 25 --output top25_tv.json

# Deep Movie Details
python -m imdb_scraper.cli details tt1375666 --output inception.json
```
