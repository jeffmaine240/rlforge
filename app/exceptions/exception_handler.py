from typing import Callable, Optional, Dict, Any
from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.base import BaseAppException
from app.utils.response import error_response



def create_exception_handler(
    status_code: int,
    default_message: str
) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: BaseAppException) -> JSONResponse:
        message = getattr(exc, "message", default_message)
        errors = getattr(exc, "errors", {})
        return error_response(
            status_code=status_code,
            message=message,
            errors=errors,
        )
    return exception_handler