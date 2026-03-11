from src.providers.base_provider import BaseProvider
from models.movie_score_model import *
import pandas as pd

class CriticAggProvider(BaseProvider):
    def __init__(self):
        super().__init__()
        self.name = "critic_agg"

    def fetch(self, url):
        return "Function to be developed"

    def transform(self, df: pd.DataFrame):
        return "Function to be developed"