from datetime import datetime

from pydantic import BaseModel


class Receipt(BaseModel):
  filename: str
  text: str
  timestamp: datetime
