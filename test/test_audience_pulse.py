import pytest
import pandas as pd
from pandas.errors import ParserError, EmptyDataError
from src.providers.audience_pulse import AudiencePulseProvider

URL_TEST_DATA_PROVIDER2 = "test/data/test_data_provider2.json"
URL_TEST_DATA_PROVIDER_INCOMPATIBLE = "test/data/test_data_provider_incompatible.jpg"
URL_TEST_DATA_PROVIDER2_EMPTY = "test/data/empty_file.json"

""" Unit tests """


def test_audience_pulse_fetch_length(test_audience_pulse_provider):
    data = test_audience_pulse_provider.fetch(URL_TEST_DATA_PROVIDER2)
    assert len(data) == 3


def test_audience_pulse_fetch_titles(test_audience_pulse_provider):
    data = test_audience_pulse_provider.fetch(URL_TEST_DATA_PROVIDER2)
    assert data.iloc[0, 0] == "The Fall"
    assert data.iloc[1, 0] == "Eternal Sunshine of the Spotless Mind"
    assert data.iloc[2, 0] == "There Will Be Blood"


def test_audience_pulse_fetch_missing_file(test_audience_pulse_provider):
    with pytest.raises(FileNotFoundError):
        test_audience_pulse_provider.fetch("data/none.csv")


def test_audience_pulse_fetch_file_unreadable(test_audience_pulse_provider):
    with pytest.raises(ValueError):
        test_audience_pulse_provider.fetch(URL_TEST_DATA_PROVIDER_INCOMPATIBLE)


def test_audience_pulse_transform_titles(test_audience_pulse_provider, test_data):
    processed_data = test_audience_pulse_provider.transform(test_data)
    assert processed_data[0].title == "The Fall"
    assert processed_data[1].title == "Eternal Sunshine Of The Spotless Mind"
    assert processed_data[2].title == "There Will Be Blood"


def test_audience_pulse_transform_preserves_row_count(
    test_audience_pulse_provider, test_data
):
    processed = test_audience_pulse_provider.transform(test_data)
    assert len(processed) == 3


def test_audience_pulse_transform_schema_mapping(test_audience_pulse_provider, test_data):
    processed = test_audience_pulse_provider.transform(test_data)
    assert hasattr(processed[0], "title")
    assert hasattr(processed[0], "year")
    assert hasattr(processed[0], "critic_score_percentage")
    assert hasattr(processed[0], "top_critic_score")
    assert hasattr(processed[0], "total_critic_reviews_counted")


def test_audience_pulse_transform_messy_data(test_audience_pulse_provider):
    messy_data = pd.DataFrame(
        {
            "title": ["  the fall  "],
            "year": [" 2006 "],
            "audience_average_score": [" 8.0 "],
            "total_audience_ratings": [" 50000 "],
            "domestic_box_office_gross": [" 2000000 "],
        }
    )
    processed = test_audience_pulse_provider.transform(messy_data)

    assert processed[0].title == "The Fall"
    assert processed[0].year == 2006


def test_audience_pulse_transform_missing_key_attribute(test_audience_pulse_provider):
    messy_data = pd.DataFrame(
        {
            "title": ["  the fall  "],
        }
    )
    with pytest.raises(AttributeError):
        test_audience_pulse_provider.transform(messy_data)


""" Integration tests """


def test_audience_pulse_integration_pipeline(test_audience_pulse_provider):
    df = test_audience_pulse_provider.fetch(URL_TEST_DATA_PROVIDER2)
    movies = test_audience_pulse_provider.transform(df)

    assert len(movies) == 3
    assert movies[0].title == "The Fall"
    assert movies[1].year == 2004
    assert movies[2].title == "There Will Be Blood"


def test_audience_pulse_integration_messy_file(test_audience_pulse_provider, tmp_path):
    test_file = tmp_path / "messy.json"
    test_file.write_text("""
        [
            {
                "title": "  the fall  ",
                "year": " 2006 ",
                "audience_average_score": " 8.0 ",
                "total_audience_ratings": " 50000 ",
                "domestic_box_office_gross": " 2000000 "
            }
        ]
        """)

    df = test_audience_pulse_provider.fetch(test_file)
    movies = test_audience_pulse_provider.transform(df)

    assert len(movies) == 1
    assert movies[0].title == "The Fall"
    assert movies[0].year == 2006
    assert movies[0].audience_average_score == 8.0
    assert movies[0].total_audience_ratings == 50000
    assert movies[0].domestic_box_office_gross == 2000000
