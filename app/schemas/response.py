from typing import Generic, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class APIResponse(GenericModel, Generic[T]):
    status: str
    status_code: int
    message: str
    data: T
