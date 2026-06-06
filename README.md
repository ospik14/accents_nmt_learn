# НМТ — бот для вивчення наголосів

Telegram-бот для підготовки до НМТ: тренування наголосів через inline-кнопки.

## Стек

- Python 3.12, aiogram 3.x
- SQLAlchemy 2.0 (async)
- SQLite або PostgreSQL

## Локальний запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# BOT_TOKEN=...

python seed.py
python main.py
```

## Docker (VPS)

```bash
git clone https://github.com/YOUR_USER/nmt-ua-bot.git
cd nmt-ua-bot

cp .env.example .env
nano .env   # BOT_TOKEN=...
```

SQLite (рекомендовано для одного бота):

```bash
docker compose up -d --build
docker compose logs -f bot
```

PostgreSQL:

```bash
# додай POSTGRES_PASSWORD і DATABASE_URL у .env
docker compose -f docker-compose.yml -f docker-compose.postgres.yml up -d --build
```

Оновлення на сервері:

```bash
git pull
docker compose up -d --build
```

Перезавантажити слова:

```bash
docker compose run --rm --entrypoint python bot seed.py --clear
docker compose restart bot
```

## Змінні середовища

| Змінна | Опис |
|--------|------|
| `BOT_TOKEN` | Токен від @BotFather |
| `DATABASE_URL` | URL БД (за замовчуванням SQLite у `data/bot.db`) |
| `DATA_DIR` | Каталог для SQLite (у Docker: `/app/data`) |
| `AUTO_SEED` | `1` — автозаповнення БД з JSON, якщо порожня |

## Формат слів (JSON)

```json
{
  "clean_word": "алгебра",
  "options": ["а́лгебра", "алге́бра", "алгебра́"],
  "correct_index": 0
}
```

## Структура

```
├── main.py
├── seed.py
├── config.py
├── Dockerfile
├── docker-compose.yml
├── bot/
│   ├── handlers/
│   ├── keyboards/
│   ├── database/
│   ├── states/
│   └── utils/
└── data/words_sample.json
```
