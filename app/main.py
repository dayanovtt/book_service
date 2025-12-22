from fastapi import FastAPI

from app.api.books import router as book_router
from app.db.session import engine
from app.db.session import Base

from app.models.book import Book
from app.models.outbox import Outbox
from app.config.settings import settings


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Book Service",
    version="1.0.0",
)

app.include_router(book_router)

@app.get("/health")
def heath_check():
    return {"status": "ok"}
