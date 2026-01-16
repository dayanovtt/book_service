from fastapi import Depends

from app.db.session import SessionLocal
from app.services.book_service import BookService
from app.uow.uow import UnitOfWork


def get_uow() -> UnitOfWork:
    return UnitOfWork(SessionLocal)


def get_book_service(
    uow: UnitOfWork = Depends(get_uow),
) -> BookService:
    return BookService(uow)

