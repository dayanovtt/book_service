from app.models.book import Book
from app.models.outbox import Outbox
from app.uow.uow import UnitOfWork


class BookService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def add_book(self, title: str, author: str, price: float) -> None:
        with self.uow as uow:
            book = Book(title=title, author=author, price=price)
            uow.book_repo.add(book)  # flush внутри repo.add

            snapshot = {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "price": float(book.price),
            }

            uow.outbox_repo.add(
                Outbox(event_type="BookAdded", payload=snapshot)
            )

    def delete_book(self, book_id: int) -> bool:
        with self.uow as uow:
            book = uow.book_repo.get_by_id(book_id)
            if not book:
                return False

            snapshot = {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "price": float(book.price),
            }

            uow.book_repo.delete(book)
            uow.outbox_repo.add(
                Outbox(event_type="BookDeleted", payload=snapshot)
            )
            return True

    def list_books(self):
        with self.uow as uow:
            return uow.book_repo.list()
