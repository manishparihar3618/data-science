import argparse
import sys
import os
import json

try:
    from .scraper import IMDbScraper
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from imdb_scraper.scraper import IMDbScraper


def main():
    parser = argparse.ArgumentParser(
        description="IMDb Complete Web Scraper CLI - Fetch Top Charts, Search, & Movie Details",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m imdb_scraper.cli top-movies --limit 50 --output top50_movies.csv
  python -m imdb_scraper.cli top-tv --limit 25 --output top25_tv.json
  python -m imdb_scraper.cli search "Oppenheimer" --limit 5
  python -m imdb_scraper.cli details tt0111161 --output shawshank.json
        """,
    )

    subparsers = parser.add_subparsers(dest="command", required=True, help="Scraper command to run")

    # Command: top-movies
    p_top_movies = subparsers.add_parser("top-movies", help="Scrape Top 250 Movies chart")
    p_top_movies.add_argument("--limit", type=int, default=250, help="Number of movies to scrape (1-250)")
    p_top_movies.add_argument("--output", "-o", type=str, help="Output file path (.csv or .json)")

    # Command: top-tv
    p_top_tv = subparsers.add_parser("top-tv", help="Scrape Top 250 TV Shows chart")
    p_top_tv.add_argument("--limit", type=int, default=250, help="Number of TV shows to scrape (1-250)")
    p_top_tv.add_argument("--output", "-o", type=str, help="Output file path (.csv or .json)")

    # Command: popular-movies
    p_pop_movies = subparsers.add_parser("popular-movies", help="Scrape Most Popular Movies chart")
    p_pop_movies.add_argument("--limit", type=int, default=100, help="Number of movies to scrape (1-100)")
    p_pop_movies.add_argument("--output", "-o", type=str, help="Output file path (.csv or .json)")

    # Command: popular-tv
    p_pop_tv = subparsers.add_parser("popular-tv", help="Scrape Most Popular TV Shows chart")
    p_pop_tv.add_argument("--limit", type=int, default=100, help="Number of TV shows to scrape (1-100)")
    p_pop_tv.add_argument("--output", "-o", type=str, help="Output file path (.csv or .json)")

    # Command: search
    p_search = subparsers.add_parser("search", help="Instant search for title/person")
    p_search.add_argument("query", type=str, help="Search term (e.g., 'Inception')")
    p_search.add_argument("--limit", type=int, default=10, help="Maximum results (default: 10)")
    p_search.add_argument("--output", "-o", type=str, help="Output file path (.csv or .json)")

    # Command: details
    p_details = subparsers.add_parser("details", help="Fetch detailed metadata for a movie or TV show")
    p_details.add_argument("id", type=str, help="IMDb ID (e.g. tt0111161) or IMDb URL")
    p_details.add_argument("--output", "-o", type=str, help="Output file path (.csv or .json)")

    args = parser.parse_args()

    with IMDbScraper() as scraper:
        if args.command == "top-movies":
            print(f"Fetching IMDb Top {args.limit} Movies...")
            data = scraper.get_top_250_movies(limit=args.limit)
            print_chart_summary(data)
            handle_export(scraper, data, args.output)

        elif args.command == "top-tv":
            print(f"Fetching IMDb Top {args.limit} TV Shows...")
            data = scraper.get_top_250_tv_shows(limit=args.limit)
            print_chart_summary(data)
            handle_export(scraper, data, args.output)

        elif args.command == "popular-movies":
            print(f"Fetching Most Popular Movies...")
            data = scraper.get_most_popular_movies(limit=args.limit)
            print_chart_summary(data)
            handle_export(scraper, data, args.output)

        elif args.command == "popular-tv":
            print(f"Fetching Most Popular TV Shows...")
            data = scraper.get_most_popular_tv_shows(limit=args.limit)
            print_chart_summary(data)
            handle_export(scraper, data, args.output)

        elif args.command == "search":
            print(f"Searching IMDb for '{args.query}'...")
            data = scraper.search(args.query, limit=args.limit)
            print_search_results(data)
            handle_export(scraper, data, args.output)

        elif args.command == "details":
            print(f"Fetching detailed metadata for '{args.id}'...")
            data = scraper.get_movie_details(args.id)
            print_movie_details(data)
            handle_export(scraper, data, args.output)


def print_chart_summary(items):
    print(f"\nSuccessfully retrieved {len(items)} items. Top 5 Preview:")
    print("-" * 75)
    print(f"{'Rank':<5} | {'Rating':<7} | {'Year':<6} | {'Title'}")
    print("-" * 75)
    for it in items[:5]:
        rank = str(it.get("rank") or "-")
        rating = str(it.get("rating") or "-")
        year = str(it.get("year") or "-")
        title = str(it.get("title") or "Unknown")
        print(f"{rank:<5} | {rating:<7} | {year:<6} | {title}")
    print("-" * 75)


def print_search_results(items):
    print(f"\nFound {len(items)} results:")
    print("-" * 80)
    print(f"{'ID':<10} | {'Type':<12} | {'Year':<6} | {'Title'} ({'Stars'})")
    print("-" * 80)
    for it in items:
        mid = str(it.get("id") or "-")
        mtype = str(it.get("type") or "title")
        year = str(it.get("year") or "-")
        title = str(it.get("title") or "Unknown")
        stars = it.get("stars", "")
        print(f"{mid:<10} | {mtype:<12} | {year:<6} | {title} {f'({stars})' if stars else ''}")
    print("-" * 80)


def print_movie_details(m):
    print("\n" + "=" * 70)
    print(f"Title:        {m.get('title')} ({m.get('release_date') or m.get('year', 'N/A')})")
    print(f"IMDb ID:      {m.get('id')} | Rating: {m.get('rating')}/10 ({m.get('vote_count'):,} votes)" if m.get('vote_count') else f"IMDb ID: {m.get('id')}")
    print(f"Metascore:    {m.get('metascore', 'N/A')}")
    print(f"Duration:     {m.get('duration', 'N/A')} ({m.get('runtime_minutes', 'N/A')} mins)")
    print(f"Certificate:  {m.get('content_rating', 'N/A')}")
    print(f"Genres:       {', '.join(m.get('genres', []))}")
    print(f"Directors:    {', '.join(m.get('directors', []))}")
    print(f"Stars:        {', '.join(m.get('stars', []))}")
    if m.get('budget'):
        print(f"Budget:       {m['budget'].get('formatted')}")
    if m.get('gross_worldwide'):
        print(f"Worldwide:    {m['gross_worldwide'].get('formatted')}")
    print(f"Storyline:    {m.get('description')}")
    print("=" * 70 + "\n")


def handle_export(scraper, data, output_path):
    if not output_path:
        return
    if output_path.lower().endswith(".json"):
        scraper.save_to_json(data, output_path)
    else:
        scraper.save_to_csv(data, output_path)


if __name__ == "__main__":
    main()
