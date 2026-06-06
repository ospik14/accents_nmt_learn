import argparse
import asyncio
import json
import sys
from pathlib import Path

from sqlalchemy import delete, select

from bot.database.models import Word
from bot.database.repository import WordRepository
from bot.database.session import async_session, init_db

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_JSON = BASE_DIR / "data" / "words_sample.json"

DEMO_WORDS: list[dict] = [
    {
        "clean_word": "алгебра",
        "options": ["а́лгебра", "алге́бра", "алгебра́"],
        "correct_index": 0,
    },
    {
        "clean_word": "квартал",
        "options": ["ква́ртал", "кварта́л", "квартáл"],
        "correct_index": 1,
    },
    {
        "clean_word": "помилка",
        "options": ["по́милка", "поми́лка", "помилка́"],
        "correct_index": 0,
    },
]


def load_from_json(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("JSON must be a list of word objects")

    for item in data:
        if not all(k in item for k in ("clean_word", "options", "correct_index")):
            raise ValueError(
                f"Invalid entry {item!r}: need clean_word, options, correct_index"
            )
        if item["correct_index"] >= len(item["options"]):
            raise ValueError(
                f"correct_index out of range for {item['clean_word']!r}"
            )

    return data


async def seed_words(
    words_data: list[dict],
    *,
    clear: bool = False,
) -> int:
    await init_db()

    async with async_session() as session:
        if clear:
            await session.execute(delete(Word))
            await session.commit()
            print("Таблицю words очищено.")

        existing = set((await session.scalars(select(Word.clean_word))).all())

        added = 0
        skipped = 0

        for item in words_data:
            clean = item["clean_word"].strip()
            if clean in existing:
                skipped += 1
                continue

            word = Word(
                clean_word=clean,
                options=item["options"],
                correct_index=item["correct_index"],
            )
            session.add(word)
            existing.add(clean)
            added += 1

        await session.commit()

    print(f"Додано: {added}, пропущено (дублікати): {skipped}")
    return added


async def seed_if_empty(words_data: list[dict]) -> int:
    await init_db()
    async with async_session() as session:
        repo = WordRepository(session)
        if await repo.count() > 0:
            print("База не порожня, seed пропущено.")
            return 0
    return await seed_words(words_data)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load words into the database")
    parser.add_argument(
        "--file",
        "-f",
        type=Path,
        default=DEFAULT_JSON,
        help=f"JSON file (default: {DEFAULT_JSON})",
    )
    parser.add_argument("--clear", action="store_true", help="Clear table before seeding")
    parser.add_argument(
        "--dict",
        dest="use_dict",
        action="store_true",
        help="Use built-in demo words",
    )
    parser.add_argument(
        "--if-empty",
        action="store_true",
        help="Seed only when the database has no words",
    )
    return parser.parse_args()


async def main() -> None:
    args = parse_args()

    if args.use_dict:
        words_data = DEMO_WORDS
    else:
        if not args.file.exists():
            print(f"Файл не знайдено: {args.file}", file=sys.stderr)
            sys.exit(1)
        words_data = load_from_json(args.file)

    if args.if_empty:
        await seed_if_empty(words_data)
    else:
        await seed_words(words_data, clear=args.clear)


if __name__ == "__main__":
    asyncio.run(main())
