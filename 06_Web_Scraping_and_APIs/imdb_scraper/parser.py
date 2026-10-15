"""
IMDb Data Parsers & Utility Functions
Provides helper functions for parsing JSON-LD, __NEXT_DATA__, and HTML elements.
"""

import re
from typing import Dict, Any, Optional, List


def parse_iso_duration(duration_str: Optional[str]) -> Dict[str, Any]:
    """
    Parses ISO-8601 duration strings like 'PT2H22M' or 'PT142M' or 'PT45M'.
    Returns a dict with formatted string, total minutes, and total seconds.
    """
    if not duration_str or not isinstance(duration_str, str):
        return {"formatted": None, "minutes": None, "seconds": None}

    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration_str)
    if not match:
        return {"formatted": duration_str, "minutes": None, "seconds": None}

    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)

    total_minutes = hours * 60 + minutes
    total_seconds = total_minutes * 60 + seconds

    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    formatted = " ".join(parts) if parts else f"{seconds}s"

    return {
        "formatted": formatted,
        "minutes": total_minutes,
        "seconds": total_seconds,
    }


def extract_imdb_id(text: str) -> Optional[str]:
    """
    Extracts IMDb ID (e.g. 'tt0111161' or 'nm0000204') from a URL or string.
    """
    if not text:
        return None
    match = re.search(r"(tt\d{7,8}|nm\d{7,8})", str(text))
    return match.group(1) if match else text.strip()


def clean_text(text: Optional[str]) -> str:
    """Removes extra whitespace, non-breaking spaces, and newlines."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", str(text)).strip()


def parse_money(money_dict: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Formats money object from IMDb GraphQL data."""
    if not money_dict or not isinstance(money_dict, dict):
        return None
    amount = money_dict.get("amount")
    currency = money_dict.get("currency", "USD")
    if amount is None:
        return None
    return {
        "amount": amount,
        "currency": currency,
        "formatted": f"{currency} {amount:,.0f}" if isinstance(amount, (int, float)) else str(amount),
    }


def parse_json_ld_movie(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parses Movie/TVSeries JSON-LD schema into a standardized dictionary.
    """
    if not data or not isinstance(data, dict):
        return {}

    duration_info = parse_iso_duration(data.get("duration"))
    rating_data = data.get("aggregateRating", {}) or {}
    
    # Actors
    actors = []
    for actor in data.get("actor", []):
        if isinstance(actor, dict) and "name" in actor:
            actors.append(actor["name"])
        elif isinstance(actor, str):
            actors.append(actor)

    # Directors
    directors = []
    for director in data.get("director", []):
        if isinstance(director, dict) and "name" in director:
            directors.append(director["name"])
        elif isinstance(director, str):
            directors.append(director)

    # Writers / Creators
    creators = []
    for creator in data.get("creator", []):
        if isinstance(creator, dict) and creator.get("@type") == "Person" and "name" in creator:
            creators.append(creator["name"])
        elif isinstance(creator, str):
            creators.append(creator)

    # Genres
    genres = data.get("genre", [])
    if isinstance(genres, str):
        genres = [genres]
    elif not isinstance(genres, list):
        genres = []

    # Keywords
    keywords_raw = data.get("keywords")
    if isinstance(keywords_raw, str):
        keywords = [k.strip() for k in keywords_raw.split(",") if k.strip()]
    elif isinstance(keywords_raw, list):
        keywords = keywords_raw
    else:
        keywords = []

    url = data.get("url", "")
    imdb_id = extract_imdb_id(url)

    trailer_url = None
    trailer_data = data.get("trailer")
    if isinstance(trailer_data, dict):
        trailer_url = trailer_data.get("url") or trailer_data.get("embedUrl")

    rating_value = rating_data.get("ratingValue")
    try:
        rating_value = float(rating_value) if rating_value is not None else None
    except (ValueError, TypeError):
        pass

    rating_count = rating_data.get("ratingCount")
    try:
        rating_count = int(rating_count) if rating_count is not None else None
    except (ValueError, TypeError):
        pass

    release_date = data.get("datePublished") or data.get("startDate") or data.get("dateCreated")

    return {
        "id": imdb_id,
        "title": data.get("name"),
        "type": data.get("@type"),
        "url": url if url.startswith("http") else f"https://www.imdb.com{url}",
        "description": data.get("description"),
        "rating": rating_value,
        "vote_count": rating_count,
        "content_rating": data.get("contentRating"),
        "duration": duration_info.get("formatted"),
        "runtime_minutes": duration_info.get("minutes"),
        "release_date": release_date,
        "genres": genres,
        "keywords": keywords,
        "directors": directors,
        "writers": creators,
        "stars": actors,
        "poster_url": data.get("image"),
        "trailer_url": trailer_url,
    }


def parse_json_ld_item_list(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Parses ItemList JSON-LD structure (used in Top 250 and chart pages).
    """
    items = []
    raw_list = data.get("itemListElement", []) if isinstance(data, dict) else []
    
    for idx, element in enumerate(raw_list, start=1):
        item = element.get("item", {}) if isinstance(element, dict) else {}
        if not item:
            continue
        
        parsed = parse_json_ld_movie(item)
        parsed["rank"] = idx
        
        # Extract 4-digit year from release_date
        rel_date = parsed.get("release_date")
        if rel_date:
            year_match = re.search(r"\b(19\d{2}|20\d{2})\b", str(rel_date))
            parsed["year"] = int(year_match.group(1)) if year_match else str(rel_date)[:4]
        else:
            parsed["year"] = None
            
        items.append(parsed)
        
    return items

