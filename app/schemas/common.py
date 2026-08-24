from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ErrorDetail(BaseModel):
    code: int
    msg: str


class APIResponse(BaseModel, Generic[T]):
    status: bool
    data: Optional[T] = None
    error: Optional[ErrorDetail] = None