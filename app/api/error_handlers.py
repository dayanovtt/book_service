from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.schemas import ErrorBody, ErrorResponse


def http_exception_handler(_: Request, exc: StarletteHTTPException) -> JSONResponse:
    payload = ErrorResponse(error=ErrorBody(message=str(exc.detail), details=None))
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump())


def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    payload = ErrorResponse(error=ErrorBody(message="Validation error", details=exc.errors()))
    return JSONResponse(status_code=422, content=payload.model_dump())
