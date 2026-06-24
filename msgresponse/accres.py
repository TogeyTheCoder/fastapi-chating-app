from .core import MessageResponseCore
from uuid import uuid4

from .type_hints import *

from typing import (
    Any,
    Literal
)

import json

class AccountResponse(MessageResponseCore):
    def signup(self, *, username: str, password: str) -> OutputStatus:
        acc_db = self._load_acc_db_json()

        account = AccountData(
            username = str(username),
            password = str(password),
            user_id = str(uuid4()),
        )

        acc_db["accounts"].append(account.model_dump())
        self._save_acc_db_json(acc_db)

        return OutputStatus(
            success=True,
            message="Account has been created.",
            data=account
        )
    
    def login(self, *, username: str, password: str) -> OutputStatus:
        acc_db = self._load_acc_db_json()

        for acc in acc_db["accounts"]:
            if acc["username"] == username and acc["password"] == password:
                session_id = str(uuid4())
                self.user_sessions[session_id] = acc["user_id"]

                return OutputStatus(
                    success=True,
                    message="Login sucessful.",
                    data={
                        "username": acc["username"],
                        "user_id": acc["user_id"],
                        "session_id": session_id
                    }
                )
            
    def fetch_user_data(self, *, username: str, fetch_data: Literal["username", "password", "user_id"]):
        acc_db = self._load_acc_db_json()

        for acc in acc_db["accounts"]:
            if acc["username"] == username:
                match fetch_data:
                    case "username":
                        return str(acc["username"])
                    case "password":
                        return str(acc["password"])
                    case "user_id":
                        return str(acc["user_id"])
                    case _:
                        raise ValueError("Please fill the arg 'fetch_data'.")

    def get_all_sessions(self) -> str:
        return json.dumps(self.user_sessions, indent=4)
