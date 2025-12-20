from sqlalchemy.orm import Session

from app.models.book import Book


class BookRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, book: Book):
        self.session.add(book)