from src.providers.critic_agg import CriticAggProvider
from src.providers.audience_pulse import AudiencePulseProvider
from src.providers.box_office_metrics import BoxOfficeMetricsProvider
from src.pipeline import MoviePipeline
import pandas as pd


def main():
    pipeline = MoviePipeline(
        providers=[
            (CriticAggProvider(), "data/input/provider1.csv"),
            (AudiencePulseProvider(), "data/input/provider2.json"),
            (
                BoxOfficeMetricsProvider(),
                {
                    "domestic": "data/input/provider3_domestic.csv",
                    "financials": "data/input/provider3_financials.csv",
                    "international": "data/input/provider3_international.csv",
                },
            ),
        ]
    )

    movies = pipeline.run()
    df = pd.DataFrame([movie.model_dump() for movie in movies])
    df.to_csv("data/output/unified_movies.csv", index=False)


if __name__ == "__main__":
    main()
