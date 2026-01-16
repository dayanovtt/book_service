from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.books import router as book_router
from app.api.error_handlers import (
    http_exception_handler,
    validation_exception_handler,
)
from app.db.session import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Book Service",
    version="1.0.0",
)

app.add_exception_handler(
    StarletteHTTPException,
    http_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.include_router(book_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
