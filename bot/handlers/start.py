from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards.main_menu import main_menu_keyboard
from bot.states.study import StudyStates

router = Router(name="start")

WELCOME_TEXT = (
    "👋 Вітаю! Я бот для підготовки до <b>НМТ</b> — тренуємо наголоси в українських словах.\n\n"
    "Обери дію в меню нижче:"
)

INFO_TEXT = (
    "ℹ️ <b>Інфо</b>\n\n"
    "Бот допомагає відпрацьовувати наголоси — типове завдання на НМТ з української мови.\n\n"
    "Обери «Вивчення наголосів», задай кількість слів у колі й відповідай кнопками."
)

SETTINGS_TEXT = (
    "⚙️ <b>Налаштування</b>\n\n"
    "Розділ у розробці. Незабаром з’являться додаткові опції."
)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_keyboard())


@router.callback_query(F.data == "menu:main")
async def show_main_menu(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(WELCOME_TEXT, reply_markup=main_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "menu:info")
async def show_info(callback: CallbackQuery) -> None:
    await callback.message.edit_text(INFO_TEXT, reply_markup=main_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "menu:settings")
async def show_settings(callback: CallbackQuery) -> None:
    await callback.message.edit_text(SETTINGS_TEXT, reply_markup=main_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "menu:study")
async def start_study_menu(callback: CallbackQuery, state: FSMContext) -> None:
    from bot.keyboards.study import count_selection_keyboard

    await state.set_state(StudyStates.choosing_count)
    await callback.message.edit_text(
        "Скільки слів хочеш пройти в цьому колі?",
        reply_markup=count_selection_keyboard(),
    )
    await callback.answer()
