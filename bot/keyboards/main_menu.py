from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📚 Вивчення наголосів",
                    callback_data="menu:study",
                )
            ],
            [
                InlineKeyboardButton(text="ℹ️ Інфо", callback_data="menu:info"),
                InlineKeyboardButton(
                    text="⚙️ Налаштування",
                    callback_data="menu:settings",
                ),
            ],
        ]
    )
