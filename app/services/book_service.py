from fastapi import HTTPException, status

from app.models.book import Book
from app.models.outbox import Outbox
from app.repositories.book_repository import BookRepository
from app.repositories.outbox_repository import OutboxRepository


class BookService:
    def __init__(
        self,
        book_repo: BookRepository,
        outbox_repo: OutboxRepository,
    ):
        self.book_repo = book_repo
        self.outbox_repo = outbox_repo

    def add_book(self, title: str, author: str, price: float) -> None:
        book = Book(
            title=title,
            author=author,
            price=price,
        )

        self.book_repo.add(book)
        self.book_repo.session.flush()

        snapshot = {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "price": float(book.price),
        }

        event = Outbox(
            event_type="BookAdded",
            payload=snapshot,
        )

        self.outbox_repo.add(event)


    def delete_book(self, book_id: int) -> None:
        book = self.book_repo.get_by_id(book_id)

        if book is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found",
            )

        snapshot = {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "price": float(book.price),
        }

        self.book_repo.delete(book)

        event = Outbox(
            event_type="BookDeleted",
            payload=snapshot,
        )

        self.outbox_repo.add(event)

    def list_books(self):
        return self.book_repo.list()
