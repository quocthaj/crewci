.PHONY: setup up down logs health test lint fmt check

setup:
	uv sync
	uv run pre-commit install

up:
	docker compose up --build -d
	@echo "CrewCI đang chạy tại http://localhost:8000 (thử: make health)"

down:
	docker compose down

logs:
	docker compose logs -f

health:
	curl -fsS http://localhost:8000/health && echo

test:
	uv run pytest -q

lint:
	uv run ruff check .
	uv run ruff format --check .

fmt:
	uv run ruff check --fix .
	uv run ruff format .

check: lint test
