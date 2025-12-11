from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from services.excel_backup import append_to_excel
from services.google_sheets import HEADERS, GoogleSheetsClient, build_row

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class SurveyStorage:
    sheets_client: GoogleSheetsClient
    local_excel_file: Optional[Path] = None

    async def persist(self, data: Dict[str, Any], user_id: int, username: Optional[str]) -> None:
        row = build_row(data, user_id, username)
        await self.sheets_client.append_row(row)

        if self.local_excel_file:
            try:
                append_to_excel(self.local_excel_file, HEADERS, row)
            except Exception as exc:
                logger.warning("Failed to append to Excel backup: %s", exc)
