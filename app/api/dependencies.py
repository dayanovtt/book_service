from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.repositories.book_repository import BookRepository
from app.repositories.outbox_repository import OutboxRepository
from app.services.book_service import BookService


def get_session() -> Session:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_book_service(
    session: Session = Depends(get_session),
) -> BookService:
    return BookService(
        book_repo=BookRepository(session),
        outbox_repo=OutboxRepository(session),
    )
