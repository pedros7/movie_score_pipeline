from src.providers.base_provider import BaseProvider
from models.movie_score_model import *
import pandas as pd
from pandas.errors import ParserError, EmptyDataError
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


    def transform(self, df: pd.DataFrame):
        return "Function to be developed"