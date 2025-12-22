from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas import BookCreate
from app.uow.uow import UnitOfWork
from app.api.dependencies import get_session, get_book_service
from app.services.book_service import BookService


router = APIRouter(
    prefix="/books",
    tags=["books"],
)

@router.post("/")
def add_book(
    data: BookCreate,
    service: BookService = Depends(get_book_service),
    session: Session = Depends(get_session),
):
    with UnitOfWork(session):
        service.add_book(
            title=data.title,
            author=data.author,
            price=data.price,
        )

    return {"status": "ok"}

@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    service: BookService = Depends(get_book_service),
    session: Session = Depends(get_session),
):
    with UnitOfWork(session):
        service.delete_book(book_id)

    return {"status": "deleted"}
