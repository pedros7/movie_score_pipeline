import pytest
import pandas as pd
from pandas.errors import ParserError, EmptyDataError
from src.providers.critic_agg import CriticAggProvider

URL_TEST_DATA_PROVIDER1 = "test/data/test_data_provider1.csv"
URL_TEST_DATA_PROVIDER1_INCOMPATIBLE = "test/data/test_data_provider1_incompatible.jpg"
URL_TEST_DATA_PROVIDER1_EMPTY = "test/data/empty_file.csv"
URL_TEST_DATA_PROVIDER1_SHORT = "test/data/test_data_provider1_short.csv"

""" Fixtures """


@pytest.fixture
def test_provider():
    return CriticAggProvider()


@pytest.fixture
def test_data():
    return pd.read_csv(URL_TEST_DATA_PROVIDER1)


""" Unit tests """


def test_critic_agg_fetch_length(test_provider):
    data = test_provider.fetch(URL_TEST_DATA_PROVIDER1)
    assert len(data) == 3


def test_critic_agg_fetch_titles(test_provider):
    data = test_provider.fetch(URL_TEST_DATA_PROVIDER1)
    assert data.iloc[0, 0] == "The Fall"
    assert data.iloc[1, 0] == "Eternal Sunshine of the Spotless Mind"
    assert data.iloc[2, 0] == "There Will Be Blood"


def test_critic_agg_fetch_missing_file(test_provider):
    with pytest.raises(FileNotFoundError):
        test_provider.fetch("data/none.csv")


def test_critic_agg_fetch_file_unreadable(test_provider):
    with pytest.raises(ParserError):
        test_provider.fetch(URL_TEST_DATA_PROVIDER1_INCOMPATIBLE)


def test_critic_agg_fetch_empty_file(test_provider):
    with pytest.raises(EmptyDataError):
        test_provider.fetch(URL_TEST_DATA_PROVIDER1_EMPTY)


def test_critic_agg_transform_titles(test_provider, test_data):
    processed_data = test_provider.transform(test_data)
    assert processed_data[0].title == "The Fall"
    assert processed_data[1].title == "Eternal Sunshine Of The Spotless Mind"
    assert processed_data[2].title == "There Will Be Blood"


def test_critic_agg_transform_preserves_row_count(test_provider, test_data):
    processed = test_provider.transform(test_data)
    assert len(processed) == 3


def test_critic_agg_transform_schema_mapping(test_provider, test_data):
    processed = test_provider.transform(test_data)
    assert hasattr(processed[0], "title")
    assert hasattr(processed[0], "year")
    assert hasattr(processed[0], "critic_score_percentage")
    assert hasattr(processed[0], "top_critic_score")
    assert hasattr(processed[0], "total_critic_reviews_counted")


def test_critic_agg_transform_messy_data(test_provider):
    messy_data = pd.DataFrame(
        {
            "movie_title": ["  the fall  "],
            "release_year": [" 2006 "],
            "critic_score_percentage": [" 63 "],
            "top_critic_score": [" 6.2 "],
            "total_critic_reviews_counted": [" 60 "],
        }
    )
    processed = test_provider.transform(messy_data)
    assert processed[0].title == "The Fall"
    assert processed[0].year == 2006


def test_critic_agg_transform_missing_key_attribute(test_provider):
    messy_data = pd.DataFrame(
        {
            "movie_title": ["  the fall  "],
        }
    )
    with pytest.raises(AttributeError):
        test_provider.transform(messy_data)


""" Integration tests """


def test_critic_agg_integration_pipeline(test_provider):
    df = test_provider.fetch(URL_TEST_DATA_PROVIDER1)
    movies = test_provider.transform(df)

    assert len(movies) == 3
    assert movies[0].title == "The Fall"
    assert movies[1].year == 2004
    assert movies[2].title == "There Will Be Blood"


def test_critic_agg_integration_messy_file(test_provider, tmp_path):
    test_file = tmp_path / "messy.csv"
    test_file.write_text(
        """movie_title,release_year,critic_score_percentage,top_critic_score,total_critic_reviews_counted
        the fall  , 2006 , 63 , 6.2 , 60
        """
    )

    df = test_provider.fetch(test_file)
    movies = test_provider.transform(df)

    assert len(movies) == 1
    assert movies[0].title == "The Fall"
    assert movies[0].top_critic_score == 6.2
    assert movies[0].total_critic_reviews_counted == 60
