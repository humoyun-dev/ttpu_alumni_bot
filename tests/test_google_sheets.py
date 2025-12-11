from datetime import datetime

from services import google_sheets as gs


class FixedDatetime(datetime):
    @classmethod
    def utcnow(cls) -> "FixedDatetime":  # type: ignore[override]
        return cls(2024, 1, 2, 3, 4, 5)


def test_format_phone_international() -> None:
    assert gs.format_phone("+998901234567") == "+998 90 123 45 67"


def test_format_phone_local_to_international() -> None:
    assert gs.format_phone("901234567") == "+998 90 123 45 67"


def test_format_phone_invalid_returns_raw() -> None:
    assert gs.format_phone("123") == "123"


def test_build_row_formats_fields(monkeypatch) -> None:
    monkeypatch.setattr(gs, "datetime", FixedDatetime)

    data = {
        "language": "en",
        "phone": "+998901234567",
        "first_name": "John",
        "last_name": "Doe",
        "student_university_id": "SE12345",
        "is_employed": True,
        "work_place": "Acme",
        "position": "Developer",
        "share_with_employer": False,
        "region": "Toshkent shahri",
        "uni_rating": "5",
        "recommend_answer": "absolutely",
        "uni_improvement_suggestions": "More labs",
    }

    row = gs.build_row(data, user_id=42, username="user42")

    assert row == [
        "2024-01-02",
        "03:04:05",
        "42",
        "user42",
        "en",
        "+998 90 123 45 67",
        "John",
        "Doe",
        "SE12345",
        "Ha",
        "Acme",
        "Developer",
        "Yo‘q",
        "Toshkent shahri",
        "5",
        "Albatta",
        "More labs",
    ]
