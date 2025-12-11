# Telegram Survey Bot

Async Telegram bot (aiogram v3) that collects alumni/graduate survey answers, writes them to Google Sheets, and can optionally keep a local Excel backup.

## Features
- Multilingual prompts (uz/ru/en) with graceful fallback.
- Guided FSM-based flow that collects contact info, student ID, employment status, ratings, recommendation, and an open-text improvement suggestion.
- Persists each submission to Google Sheets; optionally mirrors to a local `xlsx` file.
- Normalizes phone numbers to Uzbek format when possible.

## Prerequisites
- Python 3.10+
- Telegram bot token (from @BotFather)
- Google Cloud service account JSON with access to the target Sheet
- (Optional) path for a local Excel backup file

## Setup
1) Create and activate a virtualenv, then install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```
2) Copy `.env.example` to `.env` and fill in secrets:
```
TELEGRAM_BOT_TOKEN=your-bot-token
GOOGLE_SERVICE_ACCOUNT_FILE=/full/path/to/service_account.json
GOOGLE_SHEET_ID=spreadsheet_id
GOOGLE_WORKSHEET_NAME=responses   # optional; defaults to first sheet
LOCAL_EXCEL_FILE=/full/path/to/responses.xlsx   # optional
```
3) Ensure the service account email has edit access to the spreadsheet.

## Running locally
```bash
source .venv/bin/activate
python main.py
```
If Telegram returns `Unauthorized`, the token is invalid or revoked; update `TELEGRAM_BOT_TOKEN` and retry.

### Run with Docker
- Build the image: `docker build -t bot-bitiruvchi .`
- Make sure your `.env` has the required variables. Point `GOOGLE_SERVICE_ACCOUNT_FILE` (and optionally `LOCAL_EXCEL_FILE`) to paths **inside** the container (e.g. `/app/service_account.json`).
- Run the container, mounting the service account JSON (and optional local Excel backup) into those paths:
```bash
docker run --rm \
  --env-file .env \
  -v /full/path/service_account.json:/app/service_account.json:ro \
  -v /full/path/responses.xlsx:/app/responses.xlsx:rw \  # optional
  bot-bitiruvchi
```
- The bot starts with `python main.py` and loads env vars at runtime; stop it with `Ctrl+C` or `docker stop <container>`.

### Run with Docker Compose
- Ensure `.env` is filled. `GOOGLE_SERVICE_ACCOUNT_FILE` and optional `LOCAL_EXCEL_FILE` should point to `/app/service_account.json` and `/app/responses.xlsx` respectively (the paths used inside the container).
- Put your service account JSON in the project root (or update the volume path below).
- Run:
```bash
docker compose up -d --build
```
- Stop and remove: `docker compose down`

## Google Sheets setup
- The bot writes rows to `GOOGLE_SHEET_ID`, to the worksheet named `GOOGLE_WORKSHEET_NAME` (or the first sheet if not provided).
- On startup it ensures the header row matches the expected schema; if the sheet is empty it seeds it, otherwise it rewrites a mismatched header.

## Data captured (column order)
1. `date` (UTC, YYYY-MM-DD)
2. `time` (UTC, HH:MM:SS)
3. `telegram_user_id`
4. `telegram_username`
5. `language`
6. `phone` (normalized where possible)
7. `first_name`
8. `last_name`
9. `student_university_id`
10. `is_employed` (Ha/Yo‘q)
11. `work_place`
12. `position`
13. `share_with_employer` (Ha/Yo‘q)
14. `region`
15. `uni_rating` (1–5)
16. `recommend_answer` (Ha/Yo‘q/Albatta)
17. `uni_improvement_suggestions` (free text)

If `LOCAL_EXCEL_FILE` is set, the same row is appended to that file as a backup.

## Conversation flow
1. `/start` → choose language.
2. Share contact (must send via button).
3. First name, last name, student ID.
4. Employment status (yes/no); if yes, ask workplace and position.
5. Consent to share data with employers (if not employed, prior question is skipped).
6. Region selection.
7. University rating (1–5).
8. Recommendation (yes/no/absolutely).
9. Open-ended: suggestions to improve the university.
10. Thank-you message; data is persisted.

## Localization
- Strings live in `i18n.py`. Fallback language is Uzbek (`uz`) if a key or language is missing.
- To add a new language, extend `LANGUAGES` and add a translation dict with all keys.

## Project structure
```
config.py              # env settings loader
i18n.py                # translations helper (t)
keyboards.py           # reply/inline keyboards
states.py              # FSM states for the survey
handlers/start.py      # /start and language selection
handlers/survey.py     # survey flow and persistence trigger
services/google_sheets.py  # Sheets client + row builder
services/excel_backup.py   # optional Excel backup
services/storage.py    # persistence orchestrator
main.py                # application bootstrap
```

## Testing
- No automated tests are included yet; add tests under `tests/` and run with:
```bash
pytest
```
