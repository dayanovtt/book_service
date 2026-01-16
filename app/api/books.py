from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.api.dependencies import get_book_service
from app.api.schemas import BookCreate, BookRead, ErrorResponse
from app.services.book_service import BookService

router = APIRouter(prefix="/books", tags=["books"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=BookRead,
    responses={
        422: {
            "model": ErrorResponse,
            "description": "Validation error",
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error",
        },
    },
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
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Book not found",
        },
        422: {
            "model": ErrorResponse,
            "description": "Validation error",
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error",
        },
    },
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
    responses={
        500: {
            "model": ErrorResponse,
            "description": "Internal server error",
        },
    },
)
def list_books(
    service: BookService = Depends(get_book_service),
):
    return service.list_books()
