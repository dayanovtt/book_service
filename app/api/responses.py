from app.api.schemas import ErrorResponse

COMMON_ERROR_RESPONSES = {
    400: {
        "model": ErrorResponse,
        "description": "Bad request",
    },
    404: {
        "model": ErrorResponse,
        "description": "Resource not found",
    },
    422: {
        "model": ErrorResponse,
        "description": "Validation error",
    },
    500: {
        "model": ErrorResponse,
        "description": "Internal server error",
    },
}
