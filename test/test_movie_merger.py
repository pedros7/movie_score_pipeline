import pytest
from models.movie_score_model import MovieScore
from src.movie_merger import movie_merger

""" Fixtures """


@pytest.fixture
def critic_agg_movie():
    return MovieScore(
        title="The Fall",
        year=2006,
        critic_score_percentage=63,
        top_critic_score=6.2,
        total_critic_reviews_counted=60,
    )


@pytest.fixture
def audience_pulse_movie():
    return MovieScore(
        title="The Fall",
        year=2006,
        audience_average_score=8.6,
        total_audience_ratings=145000,
        domestic_box_office_gross=2200000,
    )


@pytest.fixture
def box_office_metrics_movie():
    return MovieScore(
        title="The Fall",
        year=2006,
        domestic_box_office_gross=2200000,
        international_box_office_gross=3700000,
        production_budget_usd=4000000,
        marketing_spend_usd=2000000,
    )

@pytest.fixture
def audience_pulse_movie_alt():
    return MovieScore(
        title="Eternal Sunshine of the Spotless Mind",
        year=2004,
        audience_average_score=8.4,
        total_audience_ratings=1100000,
        domestic_box_office_gross=34400000,
    )



""" Unit tests """


def test_merge_combines_fields(critic_agg_movie, audience_pulse_movie):
    pass

def test_merge_combines_different_movies(critic_agg_movie, audience_pulse_movie):
    pass

def test_merge_field_preservation(critic_agg_movie, audience_pulse_movie):
    pass

def test_merge_handles_empty_list(critic_agg_movie, audience_pulse_movie):
    pass

def test_merge_handles_three_providers(critic_agg_movie, audience_pulse_movie, box_office_metrics_movie):
    pass
