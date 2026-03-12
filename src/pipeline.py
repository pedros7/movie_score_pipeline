from typing import List
from src.movie_merger import movie_merger


class MoviePipeline:
    def __init__(self, providers):
        self.providers = providers

    def run(self):
        results = []

        for provider, source in self.providers:
            raw = provider.fetch(source)
            processed = provider.transform(raw)

            results.append(processed)

        merged = movie_merger(*results)

        return merged
