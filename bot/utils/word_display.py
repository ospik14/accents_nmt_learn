from bot.database.models import Word


def format_question_text(word: Word, current: int, total: int) -> str:
    return (
        f"📖 Слово {current} з {total}\n\n"
        f"<b>{word.clean_word}</b>\n\n"
        "Обери правильний наголос:"
    )


def format_result_text(
    word: Word,
    chosen_index: int,
    is_correct: bool,
    current: int,
    total: int,
) -> str:
    correct_option = word.options[word.correct_index]
    chosen_option = word.options[chosen_index]

    header = f"📖 Слово {current} з {total}\n\n<b>{word.clean_word}</b>\n"

    if is_correct:
        return header + f"✅ <b>Правильно!</b>\n\n{correct_option}"

    lines = [
        header,
        f"❌ <b>Неправильно</b>: {chosen_option}",
        f"✅ <b>Правильний наголос:</b> <b>{correct_option}</b>",
        "",
    ]

    return "\n".join(lines)
