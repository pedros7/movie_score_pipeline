import pytest
from src.providers.critic_agg import CriticAggProvider

URL_TEST_DATA_PROVIDER1 = "data/test_data_provider1.csv"
URL_TEST_DATA_PROVIDER1_NO_QUOTES = "data/test_data_provider1_no_quotes.csv"
URL_TEST_DATA_PROVIDER1_SHORT = "data/test_data_provider1_short.csv"

@pytest.fixture
def provider():
    return CriticAggProvider()

def test_critic_agg_fetch_length(provider):
    data = provider.fetch(URL_TEST_DATA_PROVIDER1)
    assert len(data) == 3


def test_critic_agg_fetch_titles(provider):
    data = provider.fetch(URL_TEST_DATA_PROVIDER1)
    assert data.iloc[0, 0] == "The Fall"
    assert data.iloc[1, 0] == "Eternal Sunshine of the Spotless Mind"
    assert data.iloc[2, 0] == "There Will Be Blood"


def test_critic_agg_missing_file(provider):
    with pytest.raises(FileNotFoundError):
        provider.fetch("data/none.csv")


