import pytest
import pandas as pd
from pandas.errors import ParserError, EmptyDataError
from src.providers.box_office_metrics import BoxOfficeMetricsProvider

URL_TEST_DATA_PROVIDER3_DOMESTIC = "test/data/test_data_provider3_domestic.csv"
URL_TEST_DATA_PROVIDER3_FINANCIALS = "test/data/test_data_provider3_financials.csv"
URL_TEST_DATA_PROVIDER3_INTERNATIONAL = (
    "test/data/test_data_provider3_international.csv"
)
URL_TEST_DATA_PROVIDER_INCOMPATIBLE = "test/data/test_data_provider_incompatible.jpg"
URL_TEST_DATA_PROVIDER3_EMPTY = "test/data/empty_file.csv"

""" Fixtures """


@pytest.fixture
def test_provider():
    return BoxOfficeMetricsProvider()


@pytest.fixture
def test_paths():
    paths = {
        "domestic": URL_TEST_DATA_PROVIDER3_DOMESTIC,
        "financials": URL_TEST_DATA_PROVIDER3_FINANCIALS,
        "international": URL_TEST_DATA_PROVIDER3_INTERNATIONAL,
    }
    return paths


@pytest.fixture
def test_data():
    domestic = pd.read_csv(URL_TEST_DATA_PROVIDER3_DOMESTIC)
    financials = pd.read_csv(URL_TEST_DATA_PROVIDER3_FINANCIALS)
    international = pd.read_csv(URL_TEST_DATA_PROVIDER3_INTERNATIONAL)
    return (domestic, financials, international)


""" Unit tests """


def test_critic_agg_fetch_length(test_provider, test_paths):
    domestic, financials, international = test_provider.fetch(test_paths)
    assert len(domestic) == 3
    assert len(financials) == 3
    assert len(international) == 3


def test_critic_agg_fetch_titles(test_provider, test_paths):
    domestic, financials, international = test_provider.fetch(test_paths)
    assert domestic.iloc[0, 0] == "The Fall"
    assert financials.iloc[1, 0] == "Eternal Sunshine of the Spotless Mind"
    assert international.iloc[2, 0] == "There Will Be Blood"


def test_critic_agg_fetch_missing_file(test_provider, test_paths):
    missing_file_paths = test_paths.copy()
    missing_file_paths["domestic"] = "data/none.csv"

    with pytest.raises(FileNotFoundError):
        test_provider.fetch(missing_file_paths)


def test_critic_agg_fetch_file_unreadable(test_provider, test_paths):
    unreadable_file_paths = test_paths.copy()
    unreadable_file_paths["international"] = URL_TEST_DATA_PROVIDER_INCOMPATIBLE
    with pytest.raises(ParserError):
        test_provider.fetch(unreadable_file_paths)


def test_critic_agg_fetch_empty_file(test_provider, test_paths):
    empty_file_paths = test_paths.copy()
    empty_file_paths["financials"] = URL_TEST_DATA_PROVIDER3_EMPTY
    with pytest.raises(EmptyDataError):
        test_provider.fetch(empty_file_paths)


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
    assert hasattr(processed[0], "domestic_box_office_gross")
    assert hasattr(processed[0], "international_box_office_gross")
    assert hasattr(processed[0], "production_budget_usd")
    assert hasattr(processed[0], "marketing_spend_usd")


def test_critic_agg_transform_messy_data(test_provider, test_data):
    domestic, financials, international = test_data
    messy_domestic = domestic.copy()
    messy_domestic.loc[0, "film_name"] = "  the fall  "
    messy_domestic["year_of_release"] = messy_domestic["year_of_release"].astype(object)
    messy_domestic.loc[0, "year_of_release"] = " 2006 "

    processed = test_provider.transform((messy_domestic, financials, international))
    assert processed[0].title == "The Fall"
    assert processed[0].year == 2006


def test_critic_agg_transform_missing_key_attribute(test_provider, test_data):
    domestic, financials, international = test_data
    messy_financials = financials.copy()
    messy_financials = messy_financials.drop(columns=["film_name"])

    with pytest.raises(KeyError):
        test_provider.transform((domestic, messy_financials, international))


""" Integration tests """


def test_critic_agg_integration_pipeline(test_provider, test_paths):
    df = test_provider.fetch(test_paths)
    movies = test_provider.transform(df)

    assert len(movies) == 3
    assert movies[0].title == "The Fall"
    assert movies[1].year == 2004
    assert movies[2].title == "There Will Be Blood"


def test_critic_agg_integration_messy_file(test_provider, tmp_path, test_paths):
    messy_international_file = tmp_path / "messy.csv"
    messy_international_file.write_text(
        """film_name,year_of_release,box_office_gross_usd
        the fall  , 2006 , 3700000
        """
    )
    paths = test_paths.copy()
    paths["international"] = messy_international_file

    domestic, financials, international = test_provider.fetch(paths)
    domestic = domestic.iloc[:-2].copy()
    financials = financials.iloc[:-2].copy()
    movies = test_provider.transform((domestic, financials, international))

    assert len(movies) == 1
    assert movies[0].title == "The Fall"
    assert movies[0].domestic_box_office_gross == 2200000
    assert movies[0].international_box_office_gross == 3700000
    assert movies[0].production_budget_usd == 4000000
    assert movies[0].marketing_spend_usd == 2000000
