from typing import List, Dict
from models.movie_score_model import MovieScore


def movie_merger(*provider_lists: List[MovieScore]) -> List[MovieScore]:
    movie_map: Dict[tuple, MovieScore] = {}

    for provider in provider_lists:
        movies = provider if isinstance(provider, (list, tuple)) else [provider]

        for movie in movies:
            key = (movie.title, movie.year)

            if key not in movie_map:
                movie_map[key] = movie
            else:
                existing = movie_map[key]

                for field, value in movie.model_dump().items():
                    # Quick Note: Here would be interesting to implement some kind of ConflictResolution class that
                    # would maybe prioritize according to the most recent one, or even you can specify which kind of
                    # criteria do you want it to follow. It is left out because it is out of scope for the recommended
                    # assignment time
                    if value is not None:
                        current_val = getattr(existing, field)
                        if current_val is None:
                            setattr(existing, field, value)

    return list(movie_map.values())
