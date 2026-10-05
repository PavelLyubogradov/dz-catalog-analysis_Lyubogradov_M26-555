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


def build_report(movies: list[dict]) -> None:
    """Print the full console report for the movie catalog.

    Args:
        movies: The catalog of movies to report on.
    """
    avg_rating = average_rating(movies)
    _, _, avg_age = catalog_age_stats(movies)

    print("ОТЧЕТ ПО КАТАЛОГУ")
    print(f"Средний рейтинг: {avg_rating}")
    print(f"Средний возраст фильмов: {avg_age} лет")
    print(f"257 минут: {duration_in_hours(257)}")

if __name__ == "__main__":
    build_report(movies)
