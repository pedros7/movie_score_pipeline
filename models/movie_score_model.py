from pydantic import BaseModel, Field
from typing import Optional


class MovieScore(BaseModel):
    title: str = Field(...)
    year: int = Field(..., ge=1800, le=2028)

    critic_score_percentage: Optional[float] = Field(default=None, ge=0, le=100)
    top_critic_score: Optional[float] = Field(default=None, ge=0, le=10)
    total_critic_reviews_counted: Optional[int] = Field(default=None, ge=0)
    audience_average_score: Optional[float] = Field(default=None, ge=0, le=10)
    total_audience_ratings: Optional[int] = Field(default=None, ge=0)
    domestic_box_office_gross: Optional[int] = Field(default=None, ge=0)
    international_box_office_gross: Optional[int] = Field(default=None, ge=0)
    production_budget_usd: Optional[int] = Field(default=None, ge=0)
    marketing_spend_usd: Optional[int] = Field(default=None, ge=0)
