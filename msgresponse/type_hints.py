from pydantic import BaseModel
from typing import (
    Any
)

class MessageData(BaseModel):
    user: str
    user_id: str
    msg: str
    msg_id: str

class AccountData(BaseModel):
    username: str
    password: str
    user_id: str

class OutputStatus(BaseModel):
    success: bool
    message: str
    data: Any | None

