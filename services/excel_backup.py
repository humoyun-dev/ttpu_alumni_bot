from __future__ import annotations

from pathlib import Path
from typing import Sequence

import pandas as pd


def append_to_excel(path: Path, headers: Sequence[str], row: Sequence[object]) -> None:
    data = {header: [row[idx] if idx < len(row) else ""] for idx, header in enumerate(headers)}
    df = pd.DataFrame(data)

    if path.exists():
        existing = pd.read_excel(path)
        combined = pd.concat([existing, df], ignore_index=True)
        combined.to_excel(path, index=False)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(path, index=False)
