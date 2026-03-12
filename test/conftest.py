import pytest
import pandas as pd

from src.providers.critic_agg import CriticAggProvider
from src.providers.audience_pulse import AudiencePulseProvider
from src.providers.box_office_metrics import BoxOfficeMetricsProvider
from src.pipeline import MoviePipeline
from test_critic_agg import URL_TEST_DATA_PROVIDER1
from test_audience_pulse import URL_TEST_DATA_PROVIDER2
from test_box_office_metrics import (
    URL_TEST_DATA_PROVIDER3_DOMESTIC,
    URL_TEST_DATA_PROVIDER3_FINANCIALS,
    URL_TEST_DATA_PROVIDER3_INTERNATIONAL,
)

""" Fixtures """


@pytest.fixture
def test_critic_agg_provider():
    return CriticAggProvider()


@pytest.fixture
def test_critic_agg_data():
    return pd.read_csv(URL_TEST_DATA_PROVIDER1)


@pytest.fixture
def test_audience_pulse_provider():
    return AudiencePulseProvider()


@pytest.fixture
def test_audience_pulse_data():
    return pd.read_json(URL_TEST_DATA_PROVIDER2)


@pytest.fixture
def test_box_office_metrics_provider():
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
def test_box_office_metrics_data():
    domestic = pd.read_csv(URL_TEST_DATA_PROVIDER3_DOMESTIC)
    financials = pd.read_csv(URL_TEST_DATA_PROVIDER3_FINANCIALS)
    international = pd.read_csv(URL_TEST_DATA_PROVIDER3_INTERNATIONAL)
    return (domestic, financials, international)


@pytest.fixture
def pipeline():
    providers = [
        (CriticAggProvider(), URL_TEST_DATA_PROVIDER1),
        (AudiencePulseProvider(), URL_TEST_DATA_PROVIDER2),
        (
            BoxOfficeMetricsProvider(),
            {
                "domestic": URL_TEST_DATA_PROVIDER3_DOMESTIC,
                "financials": URL_TEST_DATA_PROVIDER3_FINANCIALS,
                "international": URL_TEST_DATA_PROVIDER3_INTERNATIONAL,
            },
        ),
    ]
    return MoviePipeline(providers)