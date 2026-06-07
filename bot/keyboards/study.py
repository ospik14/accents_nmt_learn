import random

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.database.models import Word


def count_selection_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="10", callback_data="count:10"),
                InlineKeyboardButton(text="20", callback_data="count:20"),
                InlineKeyboardButton(text="50", callback_data="count:50"),
            ],
            [
                InlineKeyboardButton(
                    text="Всі доступні",
                    callback_data="count:all",
                )
            ],
            [
                InlineKeyboardButton(
                    text="◀️ Головне меню",
                    callback_data="menu:main",
                )
            ],
        ]
    )


def answer_options_keyboard(word: Word) -> InlineKeyboardMarkup:
    order = list(range(len(word.options)))
    random.shuffle(order)

    buttons = [
        [
            InlineKeyboardButton(
                text=word.options[index],
                callback_data=f"answer:{word.id}:{index}",
            )
        ]
        for index in order
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def next_word_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Наступне слово ➡️",
                    callback_data="study:next",
                )
            ]
        ]
    )


def round_finished_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏠 Повернутися в головне меню",
                    callback_data="menu:main",
                )
            ]
        ]
    )
