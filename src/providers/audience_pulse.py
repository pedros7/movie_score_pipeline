from src.providers.base_provider import BaseProvider
from models.movie_score_model import MovieScore
import pandas as pd
from pandas.errors import ParserError, EmptyDataError
from typing import List
import os
import logging


class AudiencePulseProvider(BaseProvider):
    def __init__(self):
        super().__init__()
        self.name = "audience_pulse"

    def fetch(self, url):
        if not os.path.exists(url):
            logging.error(f"File not found at path: {url}")
            raise FileNotFoundError(f"The source file at {url} does not exist.")

        try:
            data = pd.read_json(url)
        except ValueError as e:
            logging.error(f"Failed to read JSON: {e}")
            raise
        return data

    def transform(self, df: pd.DataFrame) -> List[MovieScore]:
        movie_list = []
        for row in df.itertuples(index=False):

            movie = MovieScore(
                title=row.title.strip().title(),
                year=int(str(row.year).strip()),
                audience_average_score=getattr(row, "audience_average_score", None),
                total_audience_ratings=getattr(row, "total_audience_ratings", None),
                domestic_box_office_gross=getattr(
                    row, "domestic_box_office_gross", None
                ),
            )

            movie_list.append(movie)

        return movie_list
