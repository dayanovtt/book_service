from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    price: float = Field(
        ...,
        gt=0,
        le=99_999_999.99,
        description="Book price must fit NUMERIC(10,2)",
    )


class BookRead(BaseModel):
    id: int
    title: str
    author: str
    price: float
    created_at: datetime

    class Config:
        from_attributes = True


class ErrorBody(BaseModel):
    message: str
    details: Any | None = None


class ErrorResponse(BaseModel):
    error: ErrorBody
