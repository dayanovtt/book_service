from fastapi import APIRouter, Depends
from typing import List

from app.api.dependencies import get_book_service
from app.api.schemas import BookCreate, BookRead
from app.services.book_service import BookService

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/")
def add_book(
    data: BookCreate,
    service: BookService = Depends(get_book_service),
):
    service.add_book(data.title, data.author, data.price)
    return {"status": "ok"}


@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    service: BookService = Depends(get_book_service),
):
    deleted = service.delete_book(book_id)
    if deleted:
        return {"status": "deleted"}
    return {"status": "not_found"}


@router.get("/", response_model=List[BookRead])
def list_books(
    service: BookService = Depends(get_book_service),
):
    return service.list_books()
