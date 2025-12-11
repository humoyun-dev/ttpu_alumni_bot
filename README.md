# Telegram Survey Bot

Async Telegram bot (aiogram v3) that collects graduate survey responses and stores them in Google Sheets with an optional local Excel backup.

## Prerequisites

- Python 3.10+
- Telegram Bot token
- Google Cloud service account JSON with access to the target Sheet
- (Optional) Local `.xlsx` path for backups

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env  # then fill in secrets
```

Fill the following env vars in `.env`:

- `TELEGRAM_BOT_TOKEN`
- `GOOGLE_SERVICE_ACCOUNT_FILE` (path to your service account JSON)
- `GOOGLE_SHEET_ID` (the spreadsheet ID from the URL)
- optional `GOOGLE_WORKSHEET_NAME`
- optional `LOCAL_EXCEL_FILE`

## Running

```bash
source .venv/bin/activate
python main.py
```

## Testing

```bash
source .venv/bin/activate
pytest
```

## Project structure

```
config.py              # env settings loader
i18n.py                # translations helper
keyboards.py           # reply/inline keyboards
states.py              # FSM states
handlers/              # start + survey routers
services/              # Google Sheets + Excel + persistence
main.py                # bot bootstrap
```
