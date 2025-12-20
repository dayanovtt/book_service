from fastapi import APIRouter, status

from app.api.schemas import BookCreate
from app.services.book_service import BookService


router = APIRouter(
    prefix="/books",
    tags=["books"],
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_book(payload: BookCreate):
    service = BookService()
    service.add_book(
        title=payload.title,
        author=payload.author,
        price=payload.price,
    )

@router.post("/{book_id}")
def delete_book(book_id: int):
    return {"message": f"delete book {book_id} - not implemented yet"}
