from src.providers.base_provider import BaseProvider
from models.movie_score_model import MovieScore
import pandas as pd
from pandas.errors import ParserError, EmptyDataError
from typing import List, Dict
import os
import logging


class BoxOfficeMetricsProvider(BaseProvider):
    def __init__(self):
        super().__init__()
        self.name = "box_office_metrics"

    def fetch(self, paths: Dict[str, str]) -> MovieScore:
        for name, path in paths.items():
            if not os.path.exists(path):
                logging.error(f"{name} file not found at path: {path}")
                raise FileNotFoundError(f"{name} file does not exist at {path}")

        try:
            domestic = pd.read_csv(paths["domestic"])
            financials = pd.read_csv(paths["financials"])
            international = pd.read_csv(paths["international"])
        except ParserError as e:
            logging.error(f"CSV parsing error: {e}")
            raise
        except EmptyDataError as e:
            logging.error(f"File completely empty: {e}")
            raise

        return domestic, financials, international

    def transform(self, df: pd.DataFrame) -> List[MovieScore]:
        movie_list = []
        for row in df.itertuples(index=False):

            movie = MovieScore(
                title=row.movie_title.strip().title(),
                year=int(str(row.release_year).strip()),
                domestic_box_office_gross=getattr(row, "critic_score_percentage", None),
                international_box_office_gross=getattr(row, "top_critic_score", None),
                production_budget_usd=getattr(
                    row, "total_critic_reviews_counted", None
                ),
                marketing_spend_usd=getattr(row, "total_critic_reviews_counted", None),
            )

            movie_list.append(movie)

        return movie_list
