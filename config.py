from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


@dataclass(slots=True)
class Settings:
    bot_token: str
    google_service_account_file: Path
    google_sheet_id: str
    google_worksheet_name: Optional[str]
    local_excel_file: Optional[Path]


def load_config() -> Settings:
    """Load environment variables and return typed settings."""
    load_dotenv()

    bot_token = _require_env("TELEGRAM_BOT_TOKEN")
    google_file = Path(_require_env("GOOGLE_SERVICE_ACCOUNT_FILE"))
    sheet_id = _require_env("GOOGLE_SHEET_ID")
    worksheet_name = os.getenv("GOOGLE_WORKSHEET_NAME")
    local_excel = os.getenv("LOCAL_EXCEL_FILE")
    local_excel_path = Path(local_excel) if local_excel else None

    return Settings(
        bot_token=bot_token,
        google_service_account_file=google_file.expanduser(),
        google_sheet_id=sheet_id,
        google_worksheet_name=worksheet_name,
        local_excel_file=local_excel_path.expanduser() if local_excel_path else None,
    )


def _require_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise RuntimeError(f"Environment variable {key} is required")
    return value
