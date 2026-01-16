from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.api.dependencies import get_book_service
from app.api.schemas import BookCreate, BookRead, ErrorResponse
from app.services.book_service import BookService
from app.api.responses import COMMON_ERROR_RESPONSES

router = APIRouter(prefix="/books", tags=["books"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=BookRead,
    responses=COMMON_ERROR_RESPONSES,
)
def add_book(
    data: BookCreate,
    service: BookService = Depends(get_book_service),
):
    book = service.add_book(data.title, data.author, data.price)
    return book


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=COMMON_ERROR_RESPONSES,
)
def delete_book(
    book_id: int,
    service: BookService = Depends(get_book_service),
):
    deleted = service.delete_book(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/",
    response_model=List[BookRead],
    responses=COMMON_ERROR_RESPONSES,
)
def list_books(
    service: BookService = Depends(get_book_service),
):
    return service.list_books()
