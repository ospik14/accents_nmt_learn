.PHONY: build up down logs restart seed seed-clear

build:
	docker compose build

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f bot

restart:
	docker compose restart bot

seed:
	docker compose run --rm --entrypoint python bot seed.py

seed-clear:
	docker compose run --rm --entrypoint python bot seed.py --clear
