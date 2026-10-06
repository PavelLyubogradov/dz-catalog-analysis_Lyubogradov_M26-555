"""Catalog analysis: a console report built from a list of movies."""

import math

movies = [
    {"title": "The Dune Chronicles", "year": 2021, "genres": {"sci-fi", "drama"},
     "rating": 8.6, "duration_min": 155, "actors": ["T. Chalamet", "R. Ferguson", "O. Isaac"]}, # noqa: E501
    {"title": "Kitchen Stories", "year": 2019, "genres": {"comedy", "drama"},
     "rating": 7.1, "duration_min": 98, "actors": ["A. Novak", "M. Ferguson"]},
    {"title": "silent hours", "year": 2016, "genres": {"thriller", "drama"},
     "rating": 6.4, "duration_min": 112, "actors": ["J. Bloom", "K. Lee"]},
    {"title": "Comet Racers", "year": 2023, "genres": {"sci-fi", "action"},
     "rating": 5.9, "duration_min": 101, "actors": ["O. Isaac", "P. Diaz"]},
    {"title": "The Last Bakery", "year": 2014, "genres": {"comedy"},
     "rating": 7.8, "duration_min": 89, "actors": ["A. Novak", "T. Chalamet"]},
    {"title": "midnight in oslo", "year": 2020, "genres": {"thriller", "mystery"},
     "rating": 8.9, "duration_min": 124, "actors": ["K. Lee", "R. Ferguson"]},
    {"title": "Garden of Static", "year": 2022, "genres": {"drama"},
     "rating": 4.8, "duration_min": 137, "actors": ["P. Diaz", "J. Bloom"]},
    {"title": "The Quiet Algorithm", "year": 2024, "genres": {"sci-fi", "drama"},
     "rating": 9.2, "duration_min": 118, "actors": ["M. Ferguson", "O. Isaac"]},
    {"title": "Two Left Shoes", "year": 2011, "genres": {"comedy"},
     "rating": 6.0, "duration_min": 95, "actors": ["A. Novak", "K. Lee"]},
    {"title": "Red Harbor", "year": 2018, "genres": {"action", "thriller"},
     "rating": 7.3, "duration_min": 129, "actors": ["P. Diaz", "T. Chalamet"]},
]


def average_rating(movies: list[dict]) -> float:
    """Average rating across the catalog, rounded to one decimal place.

    Args:
        movies: The catalog of movies.

    Returns:
        The mean of every movie's rating, rounded to 1 decimal place.
        Returns 0.0 when the catalog is empty.
    """
    if not movies:
        return 0.0

    return round(sum(movie["rating"] for movie in movies) / len(movies), 1)


def catalog_age_stats(
    movies: list[dict], current_year: int = 2026
) -> tuple[int, int, int]:
    """Age statistics for the catalog, in years relative to current_year.

    Args:
        movies: The catalog of movies.
        current_year: The year to measure each movie's age against.

    Returns:
        A tuple (oldest_movie_age, newest_movie_age, average_age), where
        average_age is rounded up with math.ceil.
        Returns (0, 0, 0) when the catalog is empty.
    """

    if not movies:
        return 0, 0, 0

    newest_age = current_year - movies[0]["year"]
    oldest_age = newest_age
    sum_ages = oldest_age
    for movie in movies[1:]:
        current_age = current_year - movie["year"]
        oldest_age = current_age if current_age > oldest_age else oldest_age
        newest_age = current_age if current_age < newest_age else newest_age        

        sum_ages += current_age
    average_age = math.ceil(sum_ages / len(movies))

    return oldest_age, newest_age, average_age


def duration_in_hours(minutes: int) -> str:
    """Format a duration in minutes as "<h>ч <m>м".

    Args:
        minutes: Duration in minutes.

    Returns:
        The duration formatted like "2ч 35м", using integer division for
        whole hours and the remainder for leftover minutes.
    """
    hours = minutes // 60
    leftover_minutes = minutes % 60
    return f"{hours}ч {leftover_minutes}м"


def rating_tier(rating: float) -> str:
    """Return the Russian tier label for a movie rating.
 
    Args:
        rating: A movie's rating (typically 0-10).
 
    Returns:
        "шедевр" for rating >= 9, "хорошо" for 7 <= rating < 9,
        "средне" for 5 <= rating < 7, and "слабо" for rating < 5.
    """
    if rating >= 9:
        return "шедевр"
    elif rating >= 5:
        return "хорошо" if rating >= 7 else "средне" 
    else:
        return "слабо"


def decade_label(year: int) -> str:
    """Classify a release year as new, recent, or old.
 
    Args:
        year: A movie's release year.
 
    Returns:
        "новые" for years after 2020, "недавние" for 2015-2020
        inclusive, and "старые" for years before 2015.
    """
    match year:
        case _ if year > 2020:
            return "новые"
        case _ if 2015 <= year <= 2020:
            return "недавние"
        case _:
            return "старые"


def non_comedy_titles(movies: list[dict], genre: str = "comedy") -> list[str]:
    """Return the titles of movies that do NOT belong to the given genre.

    The match against each movie's genres is case-insensitive, so
    genre="Comedy" and genre="comedy" behave the same.

    Args:
        movies: The catalog of movies.
        genre: The genre to exclude.
    """
    normalized_genre = genre.lower()
    result = []
    for movie in movies:
        genres = {genre_name.lower() for genre_name in movie["genres"]}
        if normalized_genre in genres:
            continue
        result.append(movie["title"])

    return result


def find_first_masterpiece(movies: list[dict], threshold: float = 9.0) -> str:
    """Find the first movie in catalog order rated above threshold.

    Uses a while loop with break; the loop's else clause runs only when
    no break occurred, i.e. no qualifying movie was found.

    Args:
        movies: The catalog of movies, searched in order.
        threshold: The rating a movie must exceed to qualify.

    Returns:
        The first matching movie title, or a message if none qualifies.
    """
    index = 0
    while index < len(movies):
        current_movie = movies[index]
        if current_movie["rating"] > threshold:
            result = current_movie["title"]
            break
        index += 1
    else:
        result =  "Шедевров не найдено"

    return result

def count_long_movies(movies: list[dict], threshold: int = 120) -> int:
    """Count movies longer than threshold minutes.
 
    Args:
        movies: The catalog of movies.
        threshold: Minimum duration, in minutes, to count a movie.
 
    Returns:
        The number of movies with duration_min > threshold, accumulated
        in a loop (deliberately not via sum() over a filtered list).
    """
    count = 0
    for movie in movies:
        if movie["duration_min"] > threshold:
            count += 1
    return count


def build_report(movies: list[dict]) -> None:
    """Print the full console report for the movie catalog.

    Args:
        movies: The catalog of movies to report on.
    """
    avg_rating = average_rating(movies)
    oldest_age, newest_age, avg_age = catalog_age_stats(movies)
    print()
    print("ОТЧЕТ ПО КАТАЛОГУ")
    print()
    print(f"Средний рейтинг: {avg_rating}")
    print(f"Возраст самого старого фильма: {oldest_age} лет")
    print(f"Возраст самого нового фильма: {newest_age} лет")
    print(f"Средний возраст фильмов: {avg_age} лет")
    print()

    rating_tiers = ("шедевр", "хорошо", "средне", "слабо")
    print("Фильмов по рейтинговым категориям:")
    for tier in rating_tiers:
        count = sum(rating_tier(movie["rating"]) == tier for movie in movies)
        print(f"  {tier} — {count}")
    print()

    period_labels = ("новые", "недавние", "старые")
    print("Фильмов по периодам выхода:")
    for label in period_labels:
        count = sum(decade_label(movie["year"]) == label for movie in movies)
        print(f"  {label} — {count}")
    print()

    comedy = "comedy"
    print(f"Фильмы без жанра \"{comedy}\":")
    for title in non_comedy_titles(movies, comedy):
        print(f"  - {title}")
    print()

    print(f"Первый шедевр: {find_first_masterpiece(movies)}")
    print(f"Фильмов длиннее 120 минут: {count_long_movies(movies)}")
    print()


if __name__ == "__main__":
    build_report(movies)
