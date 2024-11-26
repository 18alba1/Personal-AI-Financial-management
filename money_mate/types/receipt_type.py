from typing import Literal, Sequence

from pydantic import BaseModel, Field


ItemCategory = Literal[
    "household",
    "food",
    "transportation",
    "entertainment",
    "shopping",
    "other"
]

class Item(BaseModel):
  name: str = Field(description="The name of the item")
  price: float = Field(description="The price of the item")
  category: ItemCategory = Field(
    description="The category of the item (must be one of household, food, transportation, entertainment, shopping, other)"
  )


class Receipt(BaseModel):
  company: str = Field(description="The name of the company")
  items: Sequence[Item] = Field(description="The list of all items")
  date: str = Field(description="The date of the purchase, in YYYY-MM-DD format")
