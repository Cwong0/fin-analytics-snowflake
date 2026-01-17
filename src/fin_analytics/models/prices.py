from pydantic import BaseModel, Field
from datetime import date

class PriceIn(BaseModel):
    security_id: str = Field(min_length=1, description="Internal security identifier")
    price_date: date
    clean_price: float = Field(gt=0)
    ytm: float | None = Field(default=None, ge=0)
    source: str = Field(default="manual")
