from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.exceptions import TelegramUnauthorizedError

from config import load_config
from handlers import start_router, survey_router
from services.google_sheets import GoogleSheetsClient
from services.storage import SurveyStorage

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    config = load_config()

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    sheets_client = GoogleSheetsClient(
        service_account_file=config.google_service_account_file,
        sheet_id=config.google_sheet_id,
        worksheet_name=config.google_worksheet_name,
    )
    survey_storage = SurveyStorage(sheets_client=sheets_client, local_excel_file=config.local_excel_file)

    dp.include_router(start_router)
    dp.include_router(survey_router)

    try:
        async with Bot(token=config.bot_token) as bot:
            await bot.delete_webhook(drop_pending_updates=True)
            await dp.start_polling(bot, survey_storage=survey_storage)
    except TelegramUnauthorizedError:
        logging.error(
            "Telegram returned Unauthorized. Please double-check TELEGRAM_BOT_TOKEN is correct and not revoked."
        )


if __name__ == "__main__":
    asyncio.run(main())
