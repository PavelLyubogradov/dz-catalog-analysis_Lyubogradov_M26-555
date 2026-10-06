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


# =============================================================================
# Stage 1. Warm-up: variables, numbers, math
# =============================================================================

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


# =============================================================================
# Stage 2. Conditionals and match
# =============================================================================

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


# =============================================================================
# Stage 3. Loops
# =============================================================================

def non_comedy_titles(movies: list[dict], genre: str = "comedy") -> list[str]:
    """Return the titles of movies that do NOT belong to the given genre.

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


# =============================================================================
# Stage 4. Strings
# =============================================================================

def normalize_title(title: str) -> str:
    """Convert a title to Title Case.

    Args:
        title: A movie title in any casing.

    Returns:
        The title with each word's first letter capitalized and the rest
        lowercased, built by splitting on spaces and normalizing each word.
    """
    words = title.strip().split()
    capitalized_words = [
        word[:1].upper() + word[1:].lower() if word else word for word in words
    ]
    return " ".join(capitalized_words)


def make_slug(title: str) -> str:
    """Turn a normalized title into a URL-friendly slug.
 
    Args:
        title: A (typically already normalized) movie title.
 
    Returns:
        The title lowercased with spaces replaced by hyphens, e.g.
        "the-quiet-algorithm".
    """
    return title.lower().replace(" ", "-")


def format_report_line(movie: dict) -> str:
    """Format a single movie as one human-readable report line.
 
    Args:
        movie: A movie dict from the catalog.
 
    Returns:
        A string like '"The Quiet Algorithm" (2024) — 9.2/10, 1ч 58м,
        жанры: drama, sci-fi', with the title normalized and genres
        sorted alphabetically.
    """
    title = normalize_title(movie["title"])
    duration = duration_in_hours(movie["duration_min"])
    genres = ", ".join(sorted(movie["genres"]))
    return (
        f'"{title}" ({movie["year"]}) — '
        f'{movie["rating"]}/10, {duration}, жанры: {genres}'
    )


# =============================================================================
# Stage 5. Lists
# =============================================================================

def titles_sorted_by_rating(movies: list[dict]) -> list[str]:
    """Movie titles sorted by rating, highest first.
 
    Args:
        movies: The catalog of movies. Not modified.
 
    Returns:
        A new list of titles, sorted by descending rating.
    """
    sorted_movies = sorted(movies, key=lambda movie: movie["rating"], reverse=True)
    return [movie["title"] for movie in sorted_movies]


def top_n_by_rating(movies: list[dict], n: int = 3) -> list[tuple[str, float]]:
    """The top n movies by rating, as (title, rating) tuples.
 
    Args:
        movies: The catalog of movies.
        n: How many top movies to return.
 
    Returns:
        A list of (title, rating) tuples, highest rating first.
    """
    sorted_movies = sorted(movies, key=lambda movie: movie["rating"], reverse=True)
    return [(movie["title"], movie["rating"]) for movie in sorted_movies[:n]]


# =============================================================================
# Stage 6. Dictionaries
# =============================================================================

def count_by_genre(movies: list[dict]) -> dict[str, int]:
    """Count how many movies belong to each genre.
 
    Args:
        movies: The catalog of movies.
 
    Returns:
        A dict mapping each genre to the number of movies that include
        it, built manually with dict.get() (no collections.Counter).
    """
    counts: dict[str, int] = {}
    for movie in movies:
        for genre in movie["genres"]:
            counts[genre] = counts.get(genre, 0) + 1
    return counts


def actor_filmography(movies: list[dict]) -> dict[str, list[str]]:
    """Build a mapping of each actor to the titles they appear in.
 
    Args:
        movies: The catalog of movies.
 
    Returns:
        A dict mapping each actor's name to a list of movie titles.
    """
    filmography: dict[str, list[str]] = {}
    for movie in movies:
        for actor in movie["actors"]:
            filmography.setdefault(actor, []).append(movie["title"])
    return filmography


def above_average_ratings(movies: list[dict]) -> dict[str, float]:
    """Titles and ratings for movies rated above the catalog average.
 
    Args:
        movies: The catalog of movies.
 
    Returns:
        A dict of {title: rating}, built with a dict comprehension,
        containing only movies whose rating exceeds average_rating().
    """
    avg = average_rating(movies)
    return {
        movie["title"]: movie["rating"] for movie in movies if movie["rating"] > avg
    }


# =============================================================================
# Stage 7. Sets
# =============================================================================

def all_genres(movies: list[dict]) -> set[str]:
    """All unique genres present anywhere in the catalog.
 
    Args:
        movies: The catalog of movies.
 
    Returns:
        The union of every movie's genre set.
    """
    genres: set[str] = set()
    for movie in movies:
        genres.update(movie["genres"])
    return genres
 
 
def common_actors(movie1: dict, movie2: dict) -> set[str]:
    """Actors who appear in both movies.
 
    Args:
        movie1: The first movie.
        movie2: The second movie.
 
    Returns:
        The intersection of the two movies' actor sets.
    """
    return set(movie1["actors"]) & set(movie2["actors"])
 
 
def genres_only_in_one(movies_a: list[dict], movies_b: list[dict]) -> set[str]:
    """Genres present in movies_a but not in movies_b.
 
    Args:
        movies_a: A catalog (or slice of one) of movies.
        movies_b: Another catalog (or slice) to compare against.
 
    Returns:
        The set difference: all_genres(movies_a) - all_genres(movies_b).
    """
    return all_genres(movies_a) - all_genres(movies_b)


# =============================================================================
# Stage 8. Iterators and generators
# =============================================================================

def iter_high_rated(movies: list[dict], min_rating: float = 8.0):
    """Yields movies rated at least min_rating.
 
    Args:
        movies: The catalog of movies.
        min_rating: The minimum rating a movie must have to be yielded.
 
    Yields:
        Each movie dict with rating >= min_rating, in catalog order.
    """
    for movie in movies:
        if movie["rating"] >= min_rating:
            yield movie


def demo_iter_high_rated(movies: list[dict]) -> None:
    """Print a report line for every movie from iter_high_rated().
 
    Args:
        movies: The catalog of movies.
    """
    for movie in iter_high_rated(movies):
        print(format_report_line(movie))


def total_duration_above(movies: list[dict], min_rating: float = 7.0) -> int:
    """Total runtime, in minutes, of movies rated above min_rating.
 
    Args:
        movies: The catalog of movies.
        min_rating: The rating threshold a movie must exceed.
 
    Returns:
        The sum of duration_min for qualifying movies, computed with
        sum() over a generator expression (not a list comprehension).
    """
    return sum(
        movie["duration_min"] for movie in movies if movie["rating"] > min_rating
    )

# =============================================================================
# Stage 9. Final report
# =============================================================================

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

    print("Нормализованные названия:")
    for movie in movies:
        print(f"  {normalize_title(movie['title'])}")
    print()

    print("Итоговый список Slugs:")
    for movie in movies:
        slug = make_slug(normalize_title(movie["title"]))
        print(f"  {slug}")
    print()

    print("Форматированные строки:")
    for movie in movies:
        print(f"  {format_report_line(movie)}")
    print()

    print("Фильмы, отсортированные по рейтингу:")
    for title in titles_sorted_by_rating(movies):
        print(f"  - {title}")
    print()

    print("Топ-3 фильмов по рейтингу:")
    for title, rating in top_n_by_rating(movies):
        print(f"  - {title}: {rating}")
    print()

    print("Количество фильмов по жанрам:")
    for genre, count in sorted(count_by_genre(movies).items()):
        print(f"  - {genre}: {count}")
    print()

    print("Фильмография актеров:")
    for actor, titles in sorted(actor_filmography(movies).items()):
        titles_str = ", ".join(titles)
        print(f"  - {actor}: {titles_str}")
    print()

    print("Фильмы выше среднего рейтинга:")
    for title, rating in sorted(above_average_ratings(movies).items()):
        print(f"  - {title}: {rating}")
    print()

    print("Все жанры в каталоге:")
    for genre in sorted(all_genres(movies)):
        print(f"  - {genre}")
    print()

    print("Общие актеры у первых двух фильмов:")
    first_movie = movies[0]
    second_movie = movies[1]
    for actor in sorted(common_actors(first_movie, second_movie)):
        print(f"  - {actor}")
    print()

    print("Жанры, которые есть только в первом наборе:")
    for genre in sorted(genres_only_in_one(movies[:5], movies[5:])):
        print(f"  - {genre}")
    print()

    print("Фильмы с рейтингом не ниже 8.0:")
    for movie in iter_high_rated(movies, min_rating=8.0):
        print(f"  - {movie['title']}: {movie['rating']}")
    print()

    print("Общая длительность фильмов с рейтингом выше 7.0:")
    print(f"  {total_duration_above(movies, min_rating=7.0)} минут")
    print()

if __name__ == "__main__":
    build_report(movies)
