from difflib import get_close_matches
from typing import (
    Any,
)
import json

class MessageResponseCore:
    def _load_json(self) -> dict[str, Any]:
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_json(self, data: Any) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent= 4)

    def _load_acc_db_json(self) -> dict[str, Any]:
        with open(self.acc_db_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_acc_db_json(self, data: Any) -> None:
        with open(self.acc_db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent= 4)

    def _match_messages(self, msg: str) -> str | None:
        json_file = self._load_json()

        data = []
        for m in json_file["messages"]:
            data.append(m["msg"])

        matches = get_close_matches(msg, data, n=len(data), cutoff=0.5)
        return "\n".join(matches) if matches else None