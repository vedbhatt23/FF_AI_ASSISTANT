"""
Mock Data Generator for Secure AI Insights Assistant.

Generates 6 CSV files with realistic entertainment company data:
- movies.csv (~50 movies)
- viewers.csv (~200 viewers)
- watch_activity.csv (~2000 records)
- reviews.csv (~500 reviews)
- marketing_spend.csv (~100 campaigns)
- regional_performance.csv (~50 records)

Hard-coded titles include "Stellar Run", "Dark Orbit", "Last Kingdom"
to support the required example questions.
"""

import csv
import os
import random
from datetime import datetime, timedelta
from pathlib import Path

# Seed for reproducibility
random.seed(42)

DATA_DIR = Path(__file__).parent.parent / "data" / "csv"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ──────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────

GENRES = ["Action", "Comedy", "Drama", "Sci-Fi", "Thriller", "Romance", "Horror", "Documentary"]
LANGUAGES = ["English", "Spanish", "French", "Hindi", "Korean", "Japanese"]
CITIES = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "San Francisco", "Seattle", "Miami", "Boston", "Denver",
    "London", "Toronto", "Mumbai", "Seoul", "Tokyo",
]
DEVICES = ["Mobile", "Desktop", "Smart TV", "Tablet"]
SUBSCRIPTION_TIERS = ["Free", "Basic", "Premium", "VIP"]
MARKETING_CHANNELS = ["Social Media", "TV Ads", "Email", "Influencer", "Search Ads", "Display Ads"]

# Hard-coded movie titles to support required questions
FEATURED_TITLES = [
    ("Stellar Run", "Sci-Fi"),
    ("Dark Orbit", "Sci-Fi"),
    ("Last Kingdom", "Drama"),
    ("Neon Shadows", "Thriller"),
    ("Echoes of Tomorrow", "Drama"),
    ("Crimson Tide II", "Action"),
    ("The Final Frontier", "Sci-Fi"),
    ("Love in Paris", "Romance"),
    ("Midnight Express", "Thriller"),
    ("The Comedy Club", "Comedy"),
]

RANDOM_TITLES = [
    ("Quantum Break", "Action"), ("Silent Waters", "Drama"), ("Ghost Protocol", "Thriller"),
    ("Summer Vibes", "Comedy"), ("Iron Will", "Action"), ("Ocean's Call", "Drama"),
    ("Laugh Factory", "Comedy"), ("Red Alert", "Action"), ("Frozen Hearts", "Romance"),
    ("Dark Comedy Hour", "Comedy"), ("City Lights", "Romance"), ("Steel Rain", "Action"),
    ("The Last Joke", "Comedy"), ("Binary Stars", "Sci-Fi"), ("Haunted Manor", "Horror"),
    ("Deep Blue", "Documentary"), ("Wild Planet", "Documentary"), ("Broken Compass", "Thriller"),
    ("Funny Business", "Comedy"), ("War Zone", "Action"), ("Eternal Love", "Romance"),
    ("The Stand-up", "Comedy"), ("Mars Colony", "Sci-Fi"), ("Night Stalker", "Horror"),
    ("Nature's Fury", "Documentary"), ("Desert Storm", "Action"), ("Heartstrings", "Romance"),
    ("Cosmic Drift", "Sci-Fi"), ("The Prankster", "Comedy"), ("Shadow Ops", "Thriller"),
    ("Galactic Empire", "Sci-Fi"), ("Beach Party", "Comedy"), ("Mountain Peak", "Documentary"),
    ("Rogue Agent", "Thriller"), ("Time Warp", "Sci-Fi"), ("Secret Garden", "Romance"),
    ("Urban Legends", "Horror"), ("Code Red", "Action"), ("Happy Endings", "Comedy"),
    ("Parallel Lives", "Drama"),
]

ALL_TITLES = FEATURED_TITLES + RANDOM_TITLES
DIRECTORS = [
    "Sarah Chen", "James Rodriguez", "Priya Sharma", "Michael O'Brien",
    "Yuki Tanaka", "Carlos Mendez", "Emma Watson", "David Kim",
    "Aisha Patel", "Robert Fischer", "Lisa Park", "Ahmed Hassan",
]


def generate_movies():
    """Generate movies.csv with ~50 movies."""
    filepath = DATA_DIR / "movies.csv"
    movies = []

    for i, (title, genre) in enumerate(ALL_TITLES, start=1):
        release_year = random.choice([2023, 2024, 2025])
        release_month = random.randint(1, 12)
        release_day = random.randint(1, 28)
        release_date = f"{release_year}-{release_month:02d}-{release_day:02d}"

        budget = random.randint(5_000_000, 200_000_000)

        # Comedy intentionally gets weaker revenue for "weak comedy performance" question
        if genre == "Comedy":
            revenue = int(budget * random.uniform(0.3, 1.2))
            rating = round(random.uniform(4.0, 6.5), 1)
        elif title in ["Stellar Run", "Dark Orbit"]:
            revenue = int(budget * random.uniform(2.5, 5.0))
            rating = round(random.uniform(8.0, 9.5), 1)
        elif title == "Last Kingdom":
            revenue = int(budget * random.uniform(1.5, 3.0))
            rating = round(random.uniform(7.0, 8.5), 1)
        else:
            revenue = int(budget * random.uniform(0.8, 3.5))
            rating = round(random.uniform(5.0, 9.0), 1)

        movies.append({
            "movie_id": i,
            "title": title,
            "genre": genre,
            "release_date": release_date,
            "budget": budget,
            "revenue": revenue,
            "rating": rating,
            "director": random.choice(DIRECTORS),
            "language": random.choice(LANGUAGES),
        })

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=movies[0].keys())
        writer.writeheader()
        writer.writerows(movies)

    print(f"[OK] Generated {len(movies)} movies -> {filepath}")
    return movies


def generate_viewers():
    """Generate viewers.csv with ~200 viewers."""
    filepath = DATA_DIR / "viewers.csv"
    first_names = [
        "Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Sophia", "Mason",
        "Isabella", "William", "Mia", "James", "Charlotte", "Benjamin", "Amelia",
        "Lucas", "Harper", "Henry", "Evelyn", "Alexander", "Priya", "Raj", "Yuki",
        "Chen", "Aisha", "Omar", "Fatima", "Diego", "Sakura", "Jin",
    ]
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
        "Davis", "Rodriguez", "Martinez", "Kim", "Lee", "Park", "Chen", "Wang",
        "Patel", "Singh", "Shah", "Kumar", "Tanaka", "Ahmed", "Ali",
    ]

    viewers = []
    for i in range(1, 201):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        age = random.randint(18, 65)
        gender = random.choice(["Male", "Female", "Non-binary"])
        city = random.choice(CITIES)
        tier = random.choices(SUBSCRIPTION_TIERS, weights=[30, 35, 25, 10])[0]
        signup_year = random.choice([2022, 2023, 2024, 2025])
        signup_date = f"{signup_year}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"

        viewers.append({
            "viewer_id": i,
            "name": name,
            "age": age,
            "gender": gender,
            "city": city,
            "subscription_tier": tier,
            "signup_date": signup_date,
        })

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=viewers[0].keys())
        writer.writeheader()
        writer.writerows(viewers)

    print(f"[OK] Generated {len(viewers)} viewers -> {filepath}")
    return viewers


def generate_watch_activity(movies, viewers):
    """Generate watch_activity.csv with ~2000 records."""
    filepath = DATA_DIR / "watch_activity.csv"
    activities = []

    # Stellar Run gets disproportionately more watches (trending)
    stellar_run_id = next(m["movie_id"] for m in movies if m["title"] == "Stellar Run")
    trending_ids = [stellar_run_id]

    for i in range(1, 2001):
        viewer = random.choice(viewers)

        # 20% of activities go to trending titles
        if random.random() < 0.20:
            movie_id = random.choice(trending_ids)
        else:
            movie_id = random.choice(movies)["movie_id"]

        # Recent dates weighted more heavily for trending titles
        if movie_id in trending_ids:
            days_ago = random.randint(0, 30)
        else:
            days_ago = random.randint(0, 365)

        watch_date = (datetime(2025, 5, 1) - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        watch_duration = random.randint(15, 180)
        completed = random.random() < 0.65

        activities.append({
            "activity_id": i,
            "viewer_id": viewer["viewer_id"],
            "movie_id": movie_id,
            "watch_date": watch_date,
            "watch_duration_mins": watch_duration,
            "completed": completed,
            "device": random.choice(DEVICES),
        })

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=activities[0].keys())
        writer.writeheader()
        writer.writerows(activities)

    print(f"[OK] Generated {len(activities)} watch activities -> {filepath}")
    return activities


def generate_reviews(movies, viewers):
    """Generate reviews.csv with ~500 reviews."""
    filepath = DATA_DIR / "reviews.csv"

    positive_templates = [
        "Absolutely loved this movie! {title} was a masterpiece.",
        "Great storytelling and cinematography in {title}.",
        "{title} exceeded all my expectations. Highly recommended!",
        "One of the best {genre} films I've seen this year.",
        "The acting in {title} was phenomenal. Will watch again.",
        "A must-watch! {title} delivers on every level.",
        "Incredible visuals and plot. {title} is a gem.",
    ]

    negative_templates = [
        "Disappointing. {title} failed to deliver on its promise.",
        "The plot of {title} was predictable and boring.",
        "Not worth the hype. {title} was mediocre at best.",
        "Poor execution. {genre} deserves better than {title}.",
        "Waste of time. The acting in {title} felt forced.",
        "Couldn't finish {title}. Too slow and unengaging.",
    ]

    neutral_templates = [
        "{title} was okay. Nothing special but not terrible.",
        "Average {genre} film. {title} had some good moments.",
        "Mixed feelings about {title}. Some parts were great.",
        "{title} is a decent watch if you have nothing else.",
    ]

    reviews = []
    for i in range(1, 501):
        viewer = random.choice(viewers)
        movie = random.choice(movies)
        rating = random.randint(1, 10)

        if rating >= 7:
            template = random.choice(positive_templates)
        elif rating <= 4:
            template = random.choice(negative_templates)
        else:
            template = random.choice(neutral_templates)

        review_text = template.format(title=movie["title"], genre=movie["genre"])
        days_ago = random.randint(0, 365)
        review_date = (datetime(2025, 5, 1) - timedelta(days=days_ago)).strftime("%Y-%m-%d")

        reviews.append({
            "review_id": i,
            "viewer_id": viewer["viewer_id"],
            "movie_id": movie["movie_id"],
            "rating": rating,
            "review_text": review_text,
            "review_date": review_date,
        })

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=reviews[0].keys())
        writer.writeheader()
        writer.writerows(reviews)

    print(f"[OK] Generated {len(reviews)} reviews -> {filepath}")
    return reviews


def generate_marketing_spend(movies):
    """Generate marketing_spend.csv with ~100 campaigns."""
    filepath = DATA_DIR / "marketing_spend.csv"
    campaigns = []

    for i in range(1, 101):
        movie = random.choice(movies)
        channel = random.choice(MARKETING_CHANNELS)
        spend = random.randint(10_000, 2_000_000)
        impressions = int(spend * random.uniform(50, 200))
        clicks = int(impressions * random.uniform(0.01, 0.08))

        start_date = datetime(2025, random.randint(1, 4), random.randint(1, 28))
        end_date = start_date + timedelta(days=random.randint(7, 60))

        campaigns.append({
            "campaign_id": i,
            "movie_id": movie["movie_id"],
            "channel": channel,
            "spend_amount": spend,
            "impressions": impressions,
            "clicks": clicks,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
        })

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campaigns[0].keys())
        writer.writeheader()
        writer.writerows(campaigns)

    print(f"[OK] Generated {len(campaigns)} marketing campaigns -> {filepath}")
    return campaigns


def generate_regional_performance(movies):
    """Generate regional_performance.csv with ~50 records."""
    filepath = DATA_DIR / "regional_performance.csv"
    records = []

    for i in range(1, 51):
        movie = random.choice(movies)
        city = random.choice(CITIES)
        month = f"2025-{random.randint(1, 4):02d}"
        views = random.randint(1_000, 500_000)

        if movie["genre"] == "Comedy":
            revenue = int(views * random.uniform(1, 5))
            avg_rating = round(random.uniform(4.0, 6.0), 1)
        else:
            revenue = int(views * random.uniform(3, 15))
            avg_rating = round(random.uniform(5.5, 9.0), 1)

        records.append({
            "region_id": i,
            "movie_id": movie["movie_id"],
            "city": city,
            "views": views,
            "revenue": revenue,
            "avg_rating": avg_rating,
            "month": month,
        })

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    print(f"[OK] Generated {len(records)} regional performance records -> {filepath}")
    return records


def main():
    print("==> Generating mock data for Secure AI Insights Assistant...\n")

    movies = generate_movies()
    viewers = generate_viewers()
    generate_watch_activity(movies, viewers)
    generate_reviews(movies, viewers)
    generate_marketing_spend(movies)
    generate_regional_performance(movies)

    print(f"\n[OK] All data files generated in: {DATA_DIR}")


if __name__ == "__main__":
    main()
