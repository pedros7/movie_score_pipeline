from src.providers.base_provider import BaseProvider
from models.movie_score_model import MovieScore
import pandas as pd
from pandas.errors import ParserError, EmptyDataError
from typing import List, Dict, Tuple
import os
import logging


class BoxOfficeMetricsProvider(BaseProvider):
    def __init__(self):
        super().__init__()
        self.name = "box_office_metrics"

    def fetch(
        self, paths: Dict[str, str]
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
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

    def transform(
        self, data: Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]
    ) -> List[MovieScore]:
        domestic, financials, international = data

        for df in [domestic, financials, international]:
            df["film_name"] = df["film_name"].astype(str).str.strip().str.title()
            df["year_of_release"] = df["year_of_release"].astype(int)

        box_office_stats = domestic.merge(
            international,
            on=["film_name", "year_of_release"],
            suffixes=("_domestic", "_international"),
        )
        complete_stats = box_office_stats.merge(
            financials,
            on=["film_name", "year_of_release"],
        )

        movie_list = []

        for row in complete_stats.itertuples(index=False):

            movie = MovieScore(
                title=row.film_name,
                year=row.year_of_release,
                domestic_box_office_gross=getattr(
                    row, "box_office_gross_usd_domestic", None
                ),
                international_box_office_gross=getattr(
                    row, "box_office_gross_usd_international", None
                ),
                production_budget_usd=getattr(row, "production_budget_usd", None),
                marketing_spend_usd=getattr(row, "marketing_spend_usd", None),
            )

            movie_list.append(movie)

        return movie_list
