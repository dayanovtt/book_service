from sqlalchemy.orm import Session

from app.repositories.book_repository import BookRepository
from app.repositories.outbox_repository import OutboxRepository


class UnitOfWork:
    def __init__(self, session: Session):
        self.session = session
        self.book_repo = BookRepository(session)
        self.outbox_repo = OutboxRepository(session)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        # commit/rollback управляется зависимостью get_session()
        return False
