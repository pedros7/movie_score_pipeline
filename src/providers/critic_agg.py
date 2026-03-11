from src.providers.base_provider import BaseProvider
from models.movie_score_model import MovieScore
import pandas as pd
from pandas.errors import ParserError, EmptyDataError
from typing import List
import os
import logging


class CriticAggProvider(BaseProvider):
    def __init__(self):
        super().__init__()
        self.name = "critic_agg"

    def fetch(self, url):
        if not os.path.exists(url):
            logging.error(f"File not found at path: {url}")
            raise FileNotFoundError(f"The source file at {url} does not exist.")

        try:
            data = pd.read_csv(url)
        except ParserError as e:
            logging.error(f"Failed to read CSV: {e}")
            raise
        except EmptyDataError as e:
            logging.error(f"File completely empty: {e}")
            raise
        return data

    def transform(self, df: pd.DataFrame) -> List[MovieScore]:
        movie_list = []
        for row in df.itertuples(index=False):

            movie = MovieScore(
                title=row.movie_title.strip().title(),
                year=int(str(row.release_year).strip()),
                critic_score_percentage=getattr(row, "critic_score_percentage", None),
                top_critic_score=getattr(row, "top_critic_score", None),
                total_critic_reviews_counted=getattr(
                    row, "total_critic_reviews_counted", None
                ),
            )

            movie_list.append(movie)

        return movie_list
