from app.db.session import SessionLocal
from app.repositories.book_repository import BookRepository
from app.repositories.outbox_repository import OutboxRepository


class UnitOfWork:
    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory
        self.session = None
        self.book_repo = None
        self.outbox_repo = None

    def __enter__(self):
        self.session = self.session_factory()
        self.book_repo = BookRepository(self.session)
        self.outbox_repo = OutboxRepository(self.session)
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            if exc_type:
                self.session.rollback()
            else:
                self.session.commit()
        finally:
            self.session.close()

        # возвращаем False, чтобы FastAPI/uvicorn видел исключение и отдавал 500 при ошибках
        return False

