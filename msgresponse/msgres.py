from pathlib import Path
from typing import (
    Any,
    Literal,
    final
)
from uuid import uuid4
from .accres import AccountResponse
from .type_hints import *

#C:\Users\Thiago\OneDrive\Documents\VirtualEnv\FastAPI_Venv\venv\Scripts\Activate.ps1

@final
class MessageResponse(AccountResponse):
    """
    All funcs:

    Messaging:

    send_message()\nlist_messages()\nsearch_messages()\nedit_message()\nretrieve_message()\ndelete_messages()\ndelete_chat()

    Account and Security:

    login()\nsignup()\nfetch_user_data()\nget_all_sessions()

    """

    def __init__(
        self,
        *,
        json_msg_database_path: str | Path,
        json_acc_database_path: str | Path
    ):
        self.file_path: Path = Path(json_msg_database_path)
        self.acc_db_path: Path = Path(json_acc_database_path)
        self.user_sessions: dict[str, str] = {}

    def send_message(self, *, session_id: str, msg: str) -> OutputStatus:

        msg = str(msg)

        json_file = self._load_json()
        acc_db = self._load_acc_db_json()

        user_id = self.user_sessions.get(session_id)

        if user_id is None:
            return OutputStatus(
                success=False,
                message="Invalid session.",
                data=None
            )

        username = None

        for acc in acc_db["accounts"]:
            if acc["user_id"] == user_id:
                username = acc["username"]
                break

        user_msg = MessageData(
            user = username,
            user_id = user_id,
            msg = msg,
            msg_id = str(uuid4())
        )

        json_file["messages"].append(user_msg.model_dump())
        self._save_json(json_file)

        return OutputStatus(
            success=True,
            message="Message has been sent.",
            data=user_msg
        )

    def list_messages(self, return_type: Literal["standard_api", "(user): (msg)"]) -> dict[str, Any]:

        json_file = self._load_json()

        match return_type:
            case "standard_api":
                return {
                    "success": True,
                    "messages": json_file["messages"],
                    "count": len(json_file["messages"])
                }
            case "(user): (msg)":
                return {}

    def search_messages(self, msg: str) -> dict[str, Any]:

        matches = self._match_messages(msg=msg)

        return {
            "success": True,
            "matched_msgs": matches,
            "count": len(matches)
        }

    def edit_message(self, *, msg: str, session_id: str, msg_id: str) -> dict[str, Any]:

        user_id = self.user_sessions.get(session_id)

        if user_id is None:
            return OutputStatus(
                success=False,
                message="Invalid session.",
                data=None
            )

        msg = str(msg)
        msg_id = str(msg_id)
        
        json_file = self._load_json()

        for message in json_file["messages"]:
            if message["msg_id"] == msg_id and message["user_id"] == user_id:
                message["msg"] = msg

                self._save_json(json_file)

                return {
                    "success": True,
                    "message": "Message has been edited.",
                    "data": message
                }

        return {
            "success": False,
            "message": "Wrong ID, try again."
        }

    def retrieve_message(self, *, msg_id: str, session_id: str) -> dict[str, Any]:

        user_id = self.user_sessions.get(session_id)

        if user_id is None:
            return OutputStatus(
                success=False,
                message="Invalid session.",
                data=None
            )

        username = str(username)
        msg_id = str(msg_id)

        json_file = self._load_json()

        for message in json_file["messages"]:
            if message["msg_id"] == msg_id and message["user_id"] == user_id:
                return {
                    "success": True,
                    "message_data": message
                }

        return {
            "success": False,
            "message": "Wrong ID or username, try again."
        }

    def delete_message(self, *, msg_id: str, session_id: str) -> dict[str, Any]:

        user_id = self.user_sessions.get(session_id)

        if user_id is None:
            return OutputStatus(
                success=False,
                message="Invalid session.",
                data=None
            )

        username = str(username)
        msg_id = str(msg_id)

        json_file = self._load_json()

        for message in json_file["messages"]:
            if message["msg_id"] == msg_id and message["user_id"] == user_id:
                json_file["messages"].remove(message)
                self._save_json(json_file)

                return {
                    "success": True,
                    "message": "Message has been deleted.",
                    "deleted_message": message
                }

        return {
            "success": False,
            "message": "Wrong ID or username, try again."
        }

    def delete_chat(self) -> dict[str, Any]:
        json_file = self._load_json()

        deleted_count = len(json_file["messages"])

        json_file["messages"].clear()
        self._save_json(json_file)

        return {
            "success": True,
            "message": "Chat has been deleted.",
            "deleted_messages": deleted_count
        }