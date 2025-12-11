from __future__ import annotations

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from i18n import LANGUAGES, t
from keyboards import LANGUAGE_LABEL_TO_CODE, contact_keyboard, language_keyboard
from states import Reg

router = Router()


def _resolve_language(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip()
    if not value:
        return None
    if value in LANGUAGE_LABEL_TO_CODE:
        return LANGUAGE_LABEL_TO_CODE[value]
    normalized = value.lower()
    if normalized in LANGUAGES:
        return normalized
    return None


@router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(t("uz", "start_choose_language"), reply_markup=language_keyboard())
    await state.set_state(Reg.language)


@router.message(Reg.language)
async def handle_language_choice(message: Message, state: FSMContext) -> None:
    language = _resolve_language(message.text)
    if not language:
        await message.answer(t("uz", "language_not_supported"), reply_markup=language_keyboard())
        return

    await state.update_data(language=language)
    await message.answer(
        t(language, "ask_contact"),
        reply_markup=contact_keyboard(t(language, "share_contact")),
    )
    await state.set_state(Reg.contact)

