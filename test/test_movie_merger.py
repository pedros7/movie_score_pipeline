import pytest
from models.movie_score_model import MovieScore
from src.movie_merger import movie_merger


@pytest.fixture
def critic_agg_movie():
    return MovieScore(
        title="The Fall",
        year=2006,
        critic_score_percentage=100,
        top_critic_score=9.0,
        total_critic_reviews_counted=34,
    )


def audience_pulse_movie():
    return MovieScore(
        title="The Fall",
        year=2006,
        audience_average_score=8.6,
        total_audience_ratings=145000,
        domestic_box_office_gross=2200000,
    )


def box_office_metrics_movie():
    return MovieScore(
        title="The Fall",
        year=2006,
        domestic_box_office_gross=0,
        international_box_office_gross=90,
        production_budget_usd=10,
        marketing_spend_usd=10,
    )
