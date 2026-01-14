from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    price: float = Field(
        ...,
        gt=0,
        le=99_999_999.99,
        description="Book price must fit NUMERIC(10,2)"
    )

class BookRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author: str
    price: float
    created_at: datetime
