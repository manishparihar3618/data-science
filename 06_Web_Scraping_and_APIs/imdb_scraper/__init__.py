"""
IMDb Scraper Package
A complete, robust, modern web scraper for IMDb.
"""

from .scraper import IMDbScraper
from .browser_engine import StealthBrowser
from .parser import (
    parse_iso_duration,
    extract_imdb_id,
    parse_json_ld_movie,
    parse_json_ld_item_list,
)

__version__ = "1.0.0"
__all__ = [
    "IMDbScraper",
    "StealthBrowser",
    "parse_iso_duration",
    "extract_imdb_id",
    "parse_json_ld_movie",
    "parse_json_ld_item_list",
]
