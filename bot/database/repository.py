import random

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Word


class WordRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def count(self) -> int:
        result = await self._session.scalar(select(func.count()).select_from(Word))
        return result or 0

    async def get_by_id(self, word_id: int) -> Word | None:
        return await self._session.get(Word, word_id)

    async def get_random_words(self, limit: int) -> list[Word]:
        total = await self.count()
        if total == 0:
            return []

        actual_limit = min(limit, total)
        ids_result = await self._session.scalars(select(Word.id))
        all_ids = list(ids_result.all())
        selected_ids = random.sample(all_ids, actual_limit)

        words: list[Word] = []
        for word_id in selected_ids:
            word = await self.get_by_id(word_id)
            if word:
                words.append(word)
        random.shuffle(words)
        return words
