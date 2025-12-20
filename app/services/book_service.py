from app.models.book import Book
from app.models.outbox import Outbox
from app.repositories.book_repository import BookRepository
from app.repositories.outbox_repository import OutboxRepository
from app.uow.uow import UnitOfWork


class BookService:
    def add_book(self, title: str, author: str, price: float) -> None:
        with UnitOfWork() as uow:
            book = Book(
                title=title,
                author=author,
                price=price
            )

            BookRepository(uow.session).add(book)

            event = Outbox(
                event_type="BookAdded",
                payload={
                    "title": title,
                    "author": author,
                    "price": price
                },
            )
            OutboxRepository(uow.session).add(event)
