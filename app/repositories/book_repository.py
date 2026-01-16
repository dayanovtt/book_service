from typing import Optional
from sqlalchemy.orm import Session
from app.models.book import Book


class BookRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, book: Book) -> None:
        self.session.add(book)
        self.session.flush()

    def get_by_id(self, book_id: int) -> Optional[Book]:
        return self.session.get(Book, book_id)

    def delete(self, book: Book) -> None:
        self.session.delete(book)

    def list(self) -> list[Book]:
        return self.session.query(Book).order_by(Book.id).all()
