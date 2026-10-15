"""
IMDb Web Scraper Demonstration Script
Tests all scraper functionalities:
1. Fast Instant Search (Suggestions API)
2. Scrape Top 10 IMDb Movies (JSON-LD + NEXT_DATA)
3. Scrape Top 5 IMDb TV Shows
4. Deep scrape single movie details (e.g. Inception / Oppenheimer / Shawshank Redemption)
5. Export to CSV, JSON, and Pandas DataFrame
"""

import os
import sys

# Ensure local package path is accessible
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from imdb_scraper import IMDbScraper


def main():
    print("=" * 80)
    print("           IMDb COMPLETE WEB SCRAPER DEMONSTRATION")
    print("=" * 80)

    # Initialize scraper
    with IMDbScraper(headless=True) as scraper:

        # 1. FAST SEARCH DEMO
        print("\n[Step 1] Instant Search for 'Oppenheimer'...")
        search_results = scraper.search("Oppenheimer", limit=5)
        for res in search_results:
            print(f"  -> [{res['id']}] {res['title']} ({res['year']}) - {res['type']} | Stars: {res['stars']}")

        # 2. TOP 10 MOVIES
        print("\n[Step 2] Scraping IMDb Top 10 Movies Chart...")
        top_movies = scraper.get_top_250_movies(limit=10)
        df_movies = scraper.to_dataframe(top_movies)
        print("\nTop 10 Movies Preview (DataFrame):")
        print(df_movies[["rank", "title", "rating", "year", "duration", "content_rating"]])

        # Save to CSV and JSON
        output_csv = os.path.join(os.path.dirname(__file__), "imdb_top10_movies.csv")
        output_json = os.path.join(os.path.dirname(__file__), "imdb_top10_movies.json")
        scraper.save_to_csv(top_movies, output_csv)
        scraper.save_to_json(top_movies, output_json)

        # 3. TOP 5 TV SHOWS
        print("\n[Step 3] Scraping IMDb Top 5 TV Shows Chart...")
        top_tv = scraper.get_top_250_tv_shows(limit=5)
        df_tv = scraper.to_dataframe(top_tv)
        print("\nTop 5 TV Shows Preview (DataFrame):")
        print(df_tv[["rank", "title", "rating", "year", "genres"]])

        # 4. DEEP MOVIE DETAILS
        print("\n[Step 4] Fetching Deep Metadata for Inception (tt1375666)...")
        movie_details = scraper.get_movie_details("tt1375666")
        
        print("\n--- MOVIE METADATA ---")
        print(f"Title:         {movie_details.get('title')}")
        print(f"Original:      {movie_details.get('original_title')}")
        print(f"Release Date:  {movie_details.get('release_date')}")
        print(f"IMDb Rating:   {movie_details.get('rating')}/10 ({movie_details.get('vote_count'):,} votes)")
        print(f"Metascore:     {movie_details.get('metascore')}")
        print(f"Duration:      {movie_details.get('duration')} ({movie_details.get('runtime_minutes')} mins)")
        print(f"Certificate:   {movie_details.get('content_rating')}")
        print(f"Genres:        {', '.join(movie_details.get('genres', []))}")
        print(f"Directors:     {', '.join(movie_details.get('directors', []))}")
        print(f"Writers:       {', '.join(movie_details.get('writers', []))}")
        print(f"Stars:         {', '.join(movie_details.get('stars', []))}")
        print(f"Languages:     {', '.join(movie_details.get('spoken_languages', []))}")
        if movie_details.get("budget"):
            print(f"Budget:        {movie_details['budget'].get('formatted')}")
        if movie_details.get("gross_worldwide"):
            print(f"Gross World:   {movie_details['gross_worldwide'].get('formatted')}")
        print(f"Plot Summary:  {movie_details.get('description')}")
        print(f"Keywords:      {', '.join(movie_details.get('keywords', [])[:5])}...")
        print(f"Poster URL:    {movie_details.get('poster_url')}")
        print(f"Trailer URL:   {movie_details.get('trailer_url')}")
        print("----------------------")

        # Save single movie details to JSON
        movie_json = os.path.join(os.path.dirname(__file__), "inception_details.json")
        scraper.save_to_json(movie_details, movie_json)

    print("\n" + "=" * 80)
    print("             SCRAPING DEMONSTRATION COMPLETED SUCCESSFULLY!")
    print("=" * 80)


if __name__ == "__main__":
    main()
