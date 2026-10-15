"""
IMDb Scraper Core Module
Comprehensive web scraper for IMDb: Top 250 Movies/TV Shows, Search, and Full Title Metadata.
"""

import json
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional, Union

from .browser_engine import StealthBrowser
from .parser import (
    parse_json_ld_movie,
    parse_json_ld_item_list,
    extract_imdb_id,
    parse_money,
    clean_text,
)


class IMDbScraper:
    """
    Complete IMDb Scraper with support for:
    - Fast Title Search (via IMDb Suggestions API)
    - Top 250 Movies Chart
    - Top 250 TV Shows Chart
    - Most Popular Movies & TV Shows
    - Deep Title Metadata (Cast, Directors, Ratings, Box Office, Genres, Plot, Runtime, etc.)
    - Batch Metadata Extraction
    - Export to Pandas DataFrame, CSV, and JSON
    """

    TOP_250_MOVIES_URL = "https://www.imdb.com/chart/top/"
    TOP_250_TV_URL = "https://www.imdb.com/chart/toptv/"
    POPULAR_MOVIES_URL = "https://www.imdb.com/chart/moviemeter/"
    POPULAR_TV_URL = "https://www.imdb.com/chart/tvmeter/"
    SUGGEST_API_URL = "https://v3.sg.media-imdb.com/suggestion/x/{query}.json"

    def __init__(self, headless: bool = True, timeout: int = 30000):
        self.headless = headless
        self.timeout = timeout
        self._browser = StealthBrowser(headless=headless, timeout=timeout)
        self._session = requests.Session()
        self._session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        })

    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Instant search for movies, TV series, actors, and titles using IMDb's Suggestion API.
        No browser required — ultra-fast response.
        
        :param query: Search string (e.g. 'Inception', 'Breaking Bad', 'Nolan')
        :param limit: Maximum number of results to return (default: 10)
        :return: List of structured search result dictionaries
        """
        cleaned_query = query.strip().lower().replace(" ", "_")
        if not cleaned_query:
            return []

        url = self.SUGGEST_API_URL.format(query=cleaned_query)
        try:
            res = self._session.get(url, timeout=10)
            if res.status_code != 200:
                return []
            
            data = res.json()
            raw_results = data.get("d", [])
            results = []
            
            for item in raw_results[:limit]:
                imdb_id = item.get("id")
                title = item.get("l")
                year = item.get("y")
                type_name = item.get("q") or item.get("qid")
                stars = item.get("s")
                rank = item.get("rank")
                image_info = item.get("i", {})
                poster_url = image_info.get("imageUrl") if isinstance(image_info, dict) else None

                results.append({
                    "id": imdb_id,
                    "title": title,
                    "year": year,
                    "type": type_name,
                    "stars": stars,
                    "rank": rank,
                    "poster_url": poster_url,
                    "url": f"https://www.imdb.com/title/{imdb_id}/" if imdb_id and imdb_id.startswith("tt") else f"https://www.imdb.com/name/{imdb_id}/" if imdb_id else None,
                })

            return results
        except Exception as e:
            print(f"Search error for '{query}': {e}")
            return []

    def _scrape_chart(self, chart_url: str, limit: int = 250) -> List[Dict[str, Any]]:
        """Internal helper to scrape chart pages."""
        html_content = self._browser.get_page_content(chart_url, wait_selector="ul.ipc-metadata-list")
        soup = BeautifulSoup(html_content, "html.parser")
        
        # 1. Try structured JSON-LD ItemList
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and data.get("@type") == "ItemList":
                    items = parse_json_ld_item_list(data)
                    if items:
                        return items[:limit]
            except Exception:
                continue

        # 2. Try __NEXT_DATA__
        next_script = soup.find("script", id="__NEXT_DATA__")
        if next_script:
            try:
                nd = json.loads(next_script.string)
                chart_edges = (
                    nd.get("props", {})
                    .get("pageProps", {})
                    .get("pageData", {})
                    .get("chartTitles", {})
                    .get("edges", [])
                )
                items = []
                for edge in chart_edges[:limit]:
                    node = edge.get("node", {})
                    imdb_id = node.get("id")
                    title = node.get("titleText", {}).get("text")
                    year = node.get("releaseYear", {}).get("year")
                    rating_val = node.get("ratingsSummary", {}).get("aggregateRating")
                    vote_cnt = node.get("ratingsSummary", {}).get("voteCount")
                    runtime_sec = node.get("runtime", {}).get("seconds")
                    cert = node.get("certificate", {}).get("rating")
                    rank = edge.get("currentRank")
                    
                    runtime_mins = round(runtime_sec / 60) if runtime_sec else None
                    
                    items.append({
                        "rank": rank,
                        "id": imdb_id,
                        "title": title,
                        "year": year,
                        "rating": rating_val,
                        "vote_count": vote_cnt,
                        "runtime_minutes": runtime_mins,
                        "content_rating": cert,
                        "url": f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else None,
                    })
                if items:
                    return items
            except Exception:
                pass

        # 3. HTML parsing fallback
        items = []
        list_items = soup.select("ul.ipc-metadata-list li.ipc-metadata-list-summary-item")
        for idx, li in enumerate(list_items[:limit], start=1):
            title_el = li.select_one("h3.ipc-title__text")
            title_text = clean_text(title_el.text) if title_el else ""
            
            # Remove leading rank digits e.g. "1. The Shawshank Redemption"
            title_clean = title_text.split(". ", 1)[-1] if ". " in title_text else title_text

            link = li.select_one("a.ipc-title-link-wrapper")
            href = link["href"] if link and "href" in link.attrs else ""
            imdb_id = extract_imdb_id(href)

            rating_el = li.select_one("span.ipc-rating-star--rating")
            rating_text = rating_el.text.strip() if rating_el else None
            try:
                rating_val = float(rating_text) if rating_text else None
            except ValueError:
                rating_val = None

            items.append({
                "rank": idx,
                "id": imdb_id,
                "title": title_clean,
                "rating": rating_val,
                "url": f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else None,
            })

        return items

    def get_top_250_movies(self, limit: int = 250) -> List[Dict[str, Any]]:
        """
        Scrapes the IMDb Top 250 Movies chart.
        
        :param limit: Number of top movies to return (1-250, default: 250)
        :return: List of movie dictionaries containing rank, title, rating, year, etc.
        """
        return self._scrape_chart(self.TOP_250_MOVIES_URL, limit=limit)

    def get_top_250_tv_shows(self, limit: int = 250) -> List[Dict[str, Any]]:
        """
        Scrapes the IMDb Top 250 TV Shows chart.
        
        :param limit: Number of top TV shows to return (1-250, default: 250)
        :return: List of TV show dictionaries
        """
        return self._scrape_chart(self.TOP_250_TV_URL, limit=limit)

    def get_most_popular_movies(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Scrapes the IMDb Most Popular Movies (MovieMeter) chart.
        """
        return self._scrape_chart(self.POPULAR_MOVIES_URL, limit=limit)

    def get_most_popular_tv_shows(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Scrapes the IMDb Most Popular TV Shows (TVMeter) chart.
        """
        return self._scrape_chart(self.POPULAR_TV_URL, limit=limit)

    def get_movie_details(self, imdb_id_or_url: str) -> Dict[str, Any]:
        """
        Fetches detailed information for a specific movie or TV show.
        
        :param imdb_id_or_url: IMDb ID (e.g. 'tt0111161') or full IMDb URL
        :return: Comprehensive dictionary with title, ratings, cast, director, box office, etc.
        """
        imdb_id = extract_imdb_id(imdb_id_or_url)
        if not imdb_id:
            raise ValueError(f"Invalid IMDb ID or URL: {imdb_id_or_url}")

        url = f"https://www.imdb.com/title/{imdb_id}/"
        html_content = self._browser.get_page_content(url, wait_selector="h1")
        soup = BeautifulSoup(html_content, "html.parser")

        details: Dict[str, Any] = {"id": imdb_id, "url": url}

        # 1. Parse JSON-LD metadata
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and data.get("@type") in ["Movie", "TVSeries", "TVEpisode", "VideoGame", "CreativeWork"]:
                    details.update(parse_json_ld_movie(data))
                    break
            except Exception:
                continue

        # 2. Enrich with __NEXT_DATA__ (Box office, countries, metascore, original title)
        next_script = soup.find("script", id="__NEXT_DATA__")
        if next_script:
            try:
                nd = json.loads(next_script.string)
                main_col = nd.get("props", {}).get("pageProps", {}).get("mainColumnData", {})
                above_fold = nd.get("props", {}).get("pageProps", {}).get("aboveTheFoldData", {})

                # Metascore
                metacritic = above_fold.get("metacritic") or {}
                if metacritic and "metascore" in metacritic:
                    details["metascore"] = metacritic.get("metascore", {}).get("score")

                # Original Title
                orig_title = above_fold.get("originalTitleText", {}) or {}
                if orig_title:
                    details["original_title"] = orig_title.get("text")

                # Box office
                budget_data = main_col.get("productionBudget")
                gross_worldwide = main_col.get("worldwideGross")
                gross_domestic = main_col.get("grossDomestic")

                details["budget"] = parse_money(budget_data.get("budget")) if budget_data else None
                details["gross_worldwide"] = parse_money(gross_worldwide.get("total")) if gross_worldwide else None
                details["gross_domestic"] = parse_money(gross_domestic.get("total")) if gross_domestic else None

                # Spoken languages
                spoken_langs = [l.get("text") for l in main_col.get("spokenLanguages", {}).get("spokenLanguages", []) if l.get("text")]
                if spoken_langs:
                    details["spoken_languages"] = spoken_langs

                # Countries of origin
                countries = [c.get("text") for c in main_col.get("countriesOfOrigin", {}).get("countries", []) if c.get("text")]
                if countries:
                    details["countries_of_origin"] = countries

                # Production companies
                companies = [
                    edge.get("company", {}).get("companyText", {}).get("text")
                    for edge in main_col.get("production", {}).get("edges", [])
                    if edge.get("company", {}).get("companyText", {}).get("text")
                ]
                if companies:
                    details["production_companies"] = companies

            except Exception as e:
                details["_enrich_error"] = str(e)

        return details

    def get_batch_details(
        self,
        imdb_ids: List[str],
        delay: float = 1.0,
        show_progress: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Fetches full details for a batch of IMDb IDs with polite rate-limiting.
        
        :param imdb_ids: List of IMDb IDs
        :param delay: Seconds to wait between requests (default: 1.0s)
        :param show_progress: Print progress updates to console
        :return: List of movie detail dictionaries
        """
        results = []
        total = len(imdb_ids)
        for idx, mid in enumerate(imdb_ids, start=1):
            if show_progress:
                print(f"[{idx}/{total}] Scraping details for {mid}...")
            try:
                movie_data = self.get_movie_details(mid)
                results.append(movie_data)
            except Exception as err:
                print(f"Error scraping {mid}: {err}")
            if idx < total and delay > 0:
                time.sleep(delay)
        return results

    @staticmethod
    def to_dataframe(data: List[Dict[str, Any]]) -> pd.DataFrame:
        """Converts a list of movie/show dictionaries into a clean Pandas DataFrame."""
        df = pd.DataFrame(data)
        # Format list columns as comma-separated strings for clean CSV viewing
        for col in ["genres", "directors", "writers", "stars", "keywords", "spoken_languages", "countries_of_origin"]:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)
        return df

    @staticmethod
    def save_to_csv(data: Union[List[Dict[str, Any]], pd.DataFrame], filepath: str):
        """Exports data to CSV file."""
        if isinstance(data, list):
            df = IMDbScraper.to_dataframe(data)
        else:
            df = data
        df.to_csv(filepath, index=False, encoding="utf-8-sig")
        print(f"Successfully saved {len(df)} records to CSV: {filepath}")

    @staticmethod
    def save_to_json(data: Union[List[Dict[str, Any]], Dict[str, Any]], filepath: str, indent: int = 2):
        """Exports data to JSON file."""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
        count = len(data) if isinstance(data, list) else 1
        print(f"Successfully saved {count} records to JSON: {filepath}")

    def close(self):
        """Closes browser session."""
        self._browser.close()
        self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
