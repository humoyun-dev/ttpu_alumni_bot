from __future__ import annotations

from typing import Dict, Tuple

from aiogram.types import InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


LANGUAGE_CHOICES: Tuple[Tuple[str, str], ...] = (
    ("🇺🇿 O‘zbek", "uz"),
    ("🇷🇺 Русский", "ru"),
    ("🇬🇧 English", "en"),
)


LANGUAGE_LABEL_TO_CODE: Dict[str, str] = {label: code for label, code in LANGUAGE_CHOICES}


def language_keyboard() -> ReplyKeyboardMarkup:
    buttons = [KeyboardButton(text=label) for label, _ in LANGUAGE_CHOICES]
    return ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True, one_time_keyboard=True)


def contact_keyboard(label: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=label, request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def yes_no_inline(prefix: str, yes_label: str, no_label: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=yes_label, callback_data=f"{prefix}:yes")
    builder.button(text=no_label, callback_data=f"{prefix}:no")
    builder.adjust(2)
    return builder.as_markup()


REGION_CHOICES: Tuple[Tuple[str, str], ...] = (
    ("Toshkent shahri", "toshkent_shahri"),
    ("Andijon viloyati", "andijon"),
    ("Buxoro viloyati", "buxoro"),
    ("Farg‘ona viloyati", "fargona"),
    ("Jizzax viloyati", "jizzax"),
    ("Namangan viloyati", "namangan"),
    ("Navoiy viloyati", "navoiy"),
    ("Qashqadaryo viloyati", "qashqadaryo"),
    ("Samarqand viloyati", "samarqand"),
    ("Sirdaryo viloyati", "sirdaryo"),
    ("Surxondaryo viloyati", "surxondaryo"),
    ("Toshkent viloyati", "toshkent_vil"),
    ("Xorazm viloyati", "xorazm"),
    ("Qoraqalpog‘iston Respublikasi (avtonom)", "qoraqalpogiston"),
    ("Chet ellikman", "chet_ellikman"),
)


REGION_SLUG_TO_LABEL: Dict[str, str] = {slug: label for label, slug in REGION_CHOICES}


def region_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for label, slug in REGION_CHOICES:
        builder.button(text=label, callback_data=f"region:{slug}")
    builder.adjust(2, 3)
    return builder.as_markup()


def rating_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for rating in range(1, 6):
        builder.button(text=str(rating), callback_data=f"rating:{rating}")
    builder.adjust(5)
    return builder.as_markup()


def recommendation_keyboard(yes_label: str, no_label: str, absolutely_label: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=yes_label, callback_data="recommend:yes")
    builder.button(text=no_label, callback_data="recommend:no")
    builder.button(text=absolutely_label, callback_data="recommend:absolutely")
    builder.adjust(3)
    return builder.as_markup()
