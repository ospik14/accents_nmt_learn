from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.database.repository import WordRepository
from bot.database.session import async_session
from bot.keyboards.main_menu import main_menu_keyboard
from bot.keyboards.study import (
    answer_options_keyboard,
    count_selection_keyboard,
    next_word_keyboard,
    round_finished_keyboard,
)
from bot.states.study import StudyStates
from bot.utils.word_display import format_question_text, format_result_text

router = Router(name="study")

COUNT_MAP = {"10": 10, "20": 20, "50": 50}


async def _send_current_word(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    word_ids: list[int] = data["word_ids"]
    current_index: int = data["current_index"]
    total: int = data["total"]

    async with async_session() as session:
        repo = WordRepository(session)
        word = await repo.get_by_id(word_ids[current_index])

    if not word:
        await callback.message.edit_text(
            "Помилка: слово не знайдено в базі.",
            reply_markup=main_menu_keyboard(),
        )
        await state.clear()
        return

    text = format_question_text(word, current_index + 1, total)
    msg = await callback.message.edit_text(
        text,
        reply_markup=answer_options_keyboard(word),
    )
    await state.update_data(
        current_word_id=word.id,
        answered=False,
        message_id=msg.message_id if msg else callback.message.message_id,
    )


@router.callback_query(StudyStates.choosing_count, F.data.startswith("count:"))
async def on_count_selected(callback: CallbackQuery, state: FSMContext) -> None:
    count_key = callback.data.split(":", 1)[1]

    async with async_session() as session:
        repo = WordRepository(session)
        total_in_db = await repo.count()

        if total_in_db == 0:
            await callback.answer("У базі ще немає слів.", show_alert=True)
            return

        if count_key == "all":
            limit = total_in_db
        else:
            limit = COUNT_MAP.get(count_key, 10)

        words = await repo.get_random_words(limit)

    if not words:
        await callback.answer("Не вдалося підібрати слова.", show_alert=True)
        return

    await state.set_state(StudyStates.in_round)
    await state.update_data(
        word_ids=[w.id for w in words],
        current_index=0,
        correct_count=0,
        total=len(words),
        answered=False,
    )

    await _send_current_word(callback, state)
    await callback.answer()


@router.callback_query(StudyStates.in_round, F.data.startswith("answer:"))
async def on_answer(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()

    if data.get("answered"):
        await callback.answer("Відповідь уже зафіксована.")
        return

    _, word_id_str, option_str = callback.data.split(":")
    word_id = int(word_id_str)
    chosen_index = int(option_str)

    if word_id != data.get("current_word_id"):
        await callback.answer("Це питання вже неактуальне.")
        return

    async with async_session() as session:
        repo = WordRepository(session)
        word = await repo.get_by_id(word_id)

    if not word:
        await callback.answer("Слово не знайдено.", show_alert=True)
        return

    is_correct = chosen_index == word.correct_index
    correct_count = data["correct_count"] + (1 if is_correct else 0)
    current_index = data["current_index"]
    total = data["total"]

    text = format_result_text(
        word, chosen_index, is_correct, current_index + 1, total
    )

    await callback.message.edit_text(text, reply_markup=next_word_keyboard())
    await state.update_data(correct_count=correct_count, answered=True)
    await callback.answer("✅" if is_correct else "❌")


@router.callback_query(StudyStates.in_round, F.data == "study:next")
async def on_next_word(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    next_index = data["current_index"] + 1
    total = data["total"]
    correct_count = data["correct_count"]

    if next_index >= total:
        await state.clear()
        stats_text = (
            f"🎉 <b>Коло завершено!</b>\n\n"
            f"Твій результат: <b>{correct_count}/{total}</b> правильних"
        )
        percentage = round(correct_count / total * 100) if total else 0
        if percentage == 100:
            stats_text += "\n\n🏆 Ідеально!"
        elif percentage >= 80:
            stats_text += "\n\n👍 Чудовий результат!"
        elif percentage >= 50:
            stats_text += "\n\n💪 Непогано, продовжуй тренуватися!"
        else:
            stats_text += "\n\n📚 Ще трохи практики — і буде краще!"

        await callback.message.edit_text(
            stats_text,
            reply_markup=round_finished_keyboard(),
        )
        await callback.answer()
        return

    await state.update_data(current_index=next_index, answered=False)
    await _send_current_word(callback, state)
    await callback.answer()


@router.callback_query(StudyStates.choosing_count, F.data == "menu:main")
async def cancel_count_selection(callback: CallbackQuery, state: FSMContext) -> None:
    from bot.handlers.start import WELCOME_TEXT

    await state.clear()
    await callback.message.edit_text(WELCOME_TEXT, reply_markup=main_menu_keyboard())
    await callback.answer()
