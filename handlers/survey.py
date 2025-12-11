from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from i18n import t
from keyboards import (
    REGION_SLUG_TO_LABEL,
    contact_keyboard,
    rating_keyboard,
    recommendation_keyboard,
    region_keyboard,
    yes_no_inline,
)
from services.storage import SurveyStorage
from states import Reg

router = Router()


async def _persist(state: FSMContext, survey_storage: SurveyStorage, user_id: int, username: str | None) -> None:
    data = await state.get_data()
    await survey_storage.persist(data, user_id, username)


@router.message(Reg.contact, F.contact)
async def handle_contact(message: Message, state: FSMContext) -> None:
    language = (await state.get_data()).get("language", "uz")
    await state.update_data(phone=message.contact.phone_number, telegram_user_id=message.contact.user_id)
    await message.answer(t(language, "ask_first_name"), reply_markup=ReplyKeyboardRemove())
    await state.set_state(Reg.first_name)


@router.message(Reg.contact)
async def handle_contact_text(message: Message, state: FSMContext) -> None:
    language = (await state.get_data()).get("language", "uz")
    await message.answer(
        t(language, "contact_required"),
        reply_markup=contact_keyboard(t(language, "share_contact")),
    )


@router.message(Reg.first_name)
async def handle_first_name(message: Message, state: FSMContext) -> None:
    language = (await state.get_data()).get("language", "uz")
    await state.update_data(first_name=message.text or "")
    await message.answer(t(language, "ask_last_name"))
    await state.set_state(Reg.last_name)


@router.message(Reg.last_name)
async def handle_last_name(message: Message, state: FSMContext) -> None:
    language = (await state.get_data()).get("language", "uz")
    await state.update_data(last_name=message.text or "")
    await message.answer(t(language, "ask_student_id"))
    await state.set_state(Reg.student_id)


@router.message(Reg.student_id)
async def handle_student_id(message: Message, state: FSMContext) -> None:
    language = (await state.get_data()).get("language", "uz")
    await state.update_data(student_university_id=message.text or "")
    await message.answer(t(language, "ask_is_employed"), reply_markup=yes_no_inline("employed", t(language, "button_yes"), t(language, "button_no")))
    await state.set_state(Reg.is_employed)


@router.callback_query(Reg.is_employed, F.data.startswith("employed:"))
async def handle_is_employed(callback: CallbackQuery, state: FSMContext) -> None:
    language = (await state.get_data()).get("language", "uz")
    employed = callback.data.endswith(":yes")
    await state.update_data(is_employed=employed, share_with_employer=None)
    if employed:
        await callback.message.edit_text(t(language, "ask_work_place"))
        await state.set_state(Reg.work_place)
    else:
        await state.update_data(work_place="", position="")
        await callback.message.edit_text(
            t(language, "ask_share_with_employer"),
            reply_markup=yes_no_inline("share", t(language, "button_yes"), t(language, "button_no")),
        )
        await state.set_state(Reg.share_with_employer)
    await callback.answer()


@router.message(Reg.work_place)
async def handle_work_place(message: Message, state: FSMContext) -> None:
    language = (await state.get_data()).get("language", "uz")
    await state.update_data(work_place=message.text or "")
    await message.answer(t(language, "ask_position"))
    await state.set_state(Reg.position)


@router.message(Reg.position)
async def handle_position(message: Message, state: FSMContext) -> None:
    language = (await state.get_data()).get("language", "uz")
    await state.update_data(position=message.text or "")
    await message.answer(t(language, "ask_region"), reply_markup=region_keyboard())
    await state.set_state(Reg.region)


@router.callback_query(Reg.share_with_employer, F.data.startswith("share:"))
async def handle_share(callback: CallbackQuery, state: FSMContext) -> None:
    language = (await state.get_data()).get("language", "uz")
    share = callback.data.endswith(":yes")
    await state.update_data(share_with_employer=share)
    await callback.message.edit_text(t(language, "ask_region"), reply_markup=region_keyboard())
    await state.set_state(Reg.region)
    await callback.answer()


@router.callback_query(Reg.region, F.data.startswith("region:"))
async def handle_region(callback: CallbackQuery, state: FSMContext) -> None:
    language = (await state.get_data()).get("language", "uz")
    slug = callback.data.split(":", 1)[1]
    await state.update_data(region=REGION_SLUG_TO_LABEL.get(slug, slug))
    await callback.message.edit_text(t(language, "ask_uni_rating"), reply_markup=rating_keyboard())
    await state.set_state(Reg.uni_rating)
    await callback.answer()


@router.callback_query(Reg.uni_rating, F.data.startswith("rating:"))
async def handle_rating(callback: CallbackQuery, state: FSMContext) -> None:
    language = (await state.get_data()).get("language", "uz")
    rating_value = callback.data.split(":", 1)[1]
    if rating_value not in {"1", "2", "3", "4", "5"}:
        await callback.answer(t(language, "invalid_rating"), show_alert=True)
        return
    await state.update_data(uni_rating=rating_value)
    await callback.message.edit_text(
        t(language, "ask_recommendation"),
        reply_markup=recommendation_keyboard(
            t(language, "button_yes"),
            t(language, "button_no"),
            t(language, "button_absolutely"),
        ),
    )
    await state.set_state(Reg.recommendation)
    await callback.answer()


@router.callback_query(Reg.recommendation, F.data.startswith("recommend:"))
async def handle_recommendation(callback: CallbackQuery, state: FSMContext) -> None:
    language = (await state.get_data()).get("language", "uz")
    recommendation_value = callback.data.split(":", 1)[1]
    if recommendation_value not in {"yes", "no", "absolutely"}:
        await callback.answer(t(language, "invalid_input"), show_alert=True)
        return
    await state.update_data(recommend_answer=recommendation_value)
    await callback.message.edit_text(t(language, "ask_uni_improvement"))
    await state.set_state(Reg.uni_improvement)
    await callback.answer()


@router.message(Reg.uni_improvement)
async def handle_uni_improvement(message: Message, state: FSMContext, survey_storage: SurveyStorage) -> None:
    language = (await state.get_data()).get("language", "uz")
    await state.update_data(uni_improvement_suggestions=message.text or "")
    await _persist(state, survey_storage, message.from_user.id, message.from_user.username)
    await state.clear()
    await message.answer(t(language, "thanks"))


@router.message(Reg.finished)
async def handle_finished(message: Message) -> None:
    await message.answer("✅")
