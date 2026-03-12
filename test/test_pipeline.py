import pytest
from src.pipeline import MoviePipeline
from test_critic_agg import URL_TEST_DATA_PROVIDER1
from test_audience_pulse import URL_TEST_DATA_PROVIDER2
from test_box_office_metrics import (
    URL_TEST_DATA_PROVIDER3_DOMESTIC,
    URL_TEST_DATA_PROVIDER3_FINANCIALS,
    URL_TEST_DATA_PROVIDER3_INTERNATIONAL,
)


def test_pipeline_runs(
    test_critic_agg_provider, test_provider2, test_provider3, test_paths
):
    pipeline = MoviePipeline(
        providers=[
            (test_critic_agg_provider, URL_TEST_DATA_PROVIDER1),
            (test_provider2, URL_TEST_DATA_PROVIDER2),
            (test_provider3, test_paths),
        ]
    )

    result = pipeline.run()

    assert len(result) > 0


def test_pipeline_merges_data(pipeline):
    movies = pipeline.run()

    movie = movies[0]

    assert movie.title is not None
    assert movie.year is not None

    assert (
        movie.critic_score_percentage
        or movie.audience_average_score
        or movie.production_budget_usd
    )


def test_pipeline_accepts_variable_providers(test_critic_agg_provider):

    pipeline = MoviePipeline(
        providers=[
            (test_critic_agg_provider, URL_TEST_DATA_PROVIDER1),
        ]
    )

    result = pipeline.run()

    assert len(result) > 0
