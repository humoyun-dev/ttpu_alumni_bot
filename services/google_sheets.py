from __future__ import annotations

import asyncio
from datetime import datetime
from pathlib import Path
from typing import List, Mapping, Optional, Sequence

import gspread
from gspread import Spreadsheet, Worksheet

HEADERS: List[str] = [
    "date",
    "time",
    "telegram_user_id",
    "telegram_username",
    "language",
    "phone",
    "first_name",
    "last_name",
    "student_university_id",
    "is_employed",
    "work_place",
    "position",
    "share_with_employer",
    "region",
    "uni_rating",
    "recommend_answer",
    "uni_improvement_suggestions",
]


def format_bool_uz(value: bool | None) -> str:
    if value is None:
        return ""
    return "Ha" if value else "Yo‘q"


def format_phone(raw: str | None) -> str:
    if not raw:
        return ""
    digits = "".join(ch for ch in raw if ch.isdigit())

    if digits.startswith("998") and len(digits) == 12:
        pass
    elif digits.startswith("8") and len(digits) == 12:
        digits = "998" + digits[1:]
    elif len(digits) == 9 and digits[0] in ("9", "8"):
        digits = "998" + digits[-9:]

    if len(digits) == 12 and digits.startswith("998"):
        cc = digits[0:3]
        op = digits[3:5]
        p1 = digits[5:8]
        p2 = digits[8:10]
        p3 = digits[10:12]
        return f"+{cc} {op} {p1} {p2} {p3}"

    return raw


def _format_recommend_answer(value: str | None) -> str:
    if not value:
        return ""
    normalized = value.strip().lower()
    if normalized in ("yes", "ha"):
        return "Ha"
    if normalized in ("no", "yoq", "yo‘q", "yo'q"):
        return "Yo‘q"
    if normalized in ("absolutely", "albatta"):
        return "Albatta"
    return value


def build_row(data: Mapping[str, object], user_id: int, username: Optional[str]) -> List[str]:
    now = datetime.utcnow()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    language = data.get("language", "uz") or ""
    phone = format_phone(data.get("phone"))
    first_name = data.get("first_name", "") or ""
    last_name = data.get("last_name", "") or ""
    student_id = data.get("student_university_id", "") or ""
    is_employed = data.get("is_employed")
    work_place = data.get("work_place", "")
    position = data.get("position", "")
    share_with = data.get("share_with_employer")
    region = data.get("region", "") or ""
    uni_rating = data.get("uni_rating")
    recommend = _format_recommend_answer(data.get("recommend_answer"))
    uni_improvement = data.get("uni_improvement_suggestions", "") or ""

    return [
        date_str,
        time_str,
        str(user_id),
        username or "",
        str(language),
        phone,
        str(first_name),
        str(last_name),
        str(student_id),
        format_bool_uz(is_employed if isinstance(is_employed, bool) else None),
        work_place,
        position,
        format_bool_uz(share_with if isinstance(share_with, bool) else None),
        str(region),
        str(uni_rating) if uni_rating is not None else "",
        str(recommend),
        str(uni_improvement),
    ]


class GoogleSheetsClient:
    def __init__(self, service_account_file: str | Path, sheet_id: str, worksheet_name: Optional[str] = None) -> None:
        self._sheet_id = sheet_id
        self._worksheet_name = worksheet_name
        self._client = gspread.service_account(filename=str(service_account_file))
        self._worksheet = self._open_worksheet()
        self._ensure_header()

    def _open_worksheet(self) -> Worksheet:
        spreadsheet: Spreadsheet = self._client.open_by_key(self._sheet_id)
        if self._worksheet_name:
            return spreadsheet.worksheet(self._worksheet_name)
        return spreadsheet.sheet1

    def _ensure_header(self) -> None:
        values = self._worksheet.row_values(1)
        if not values:
            self._worksheet.append_row(HEADERS, value_input_option="USER_ENTERED")
        elif values != HEADERS:
            self._worksheet.delete_rows(1)
            self._worksheet.insert_row(HEADERS, 1, value_input_option="USER_ENTERED")

    async def append_row(self, values: Sequence[str]) -> None:
        await asyncio.to_thread(self._worksheet.append_row, list(values), value_input_option="USER_ENTERED")
