from pydantic import BaseModel, Field
from typing import List, Optional, Union, TypeVar
from enum import Enum
T = TypeVar('T')


class BaseResponse(BaseModel):
    message: str = Field(..., example="Document added successfully.")
    data: Optional[T] = Field(None, example=None)
    code: int = Field(..., example=200)


class BaseRequest(BaseModel):
    rust_code: str = Field(..., example="fn main() { println!(\"Hello, world!\"); }")

