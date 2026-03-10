from dataclasses import dataclass
from typing import Optional

@dataclass
class MovieScore:
    title: str
    year: int

    critic_score_percentage: Optional[float] = None
    top_critic_score: Optional[float] = None
    total_critic_reviews_counted: Optional[int] = None
    audience_average_score: Optional[float] = None
    total_audience_ratings: Optional[int] = None
    domestic_box_office_gross: Optional[int] = None
    financials_box_office_gross: Optional[int] = None
    production_budget_usd: Optional[int] = None
    marketing_spend_usd: Optional[int] = None