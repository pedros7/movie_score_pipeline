from base_provider import BaseProvider

class CriticAggProvider(BaseProvider):
    def __init__(self):
        super().__init__()
        self.name = "critic_agg"

    def fetch(self, url):
        return "Function to be developed"