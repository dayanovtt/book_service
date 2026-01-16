from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.book import Book


class BookRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, book: Book) -> None:
        self.session.add(book)
        self.session.flush()          # получаем book.id
        self.session.refresh(book)    # подтягиваем created_at (server_default)

    def delete(self, book: Book) -> None:
        self.session.delete(book)

    def get_by_id(self, book_id: int) -> Book | None:
        stmt = select(Book).where(Book.id == book_id)
        return self.session.execute(stmt).scalar_one_or_none()

    def list(self) -> list[Book]:
        stmt = select(Book).order_by(Book.id)
        return list(self.session.execute(stmt).scalars().all())
