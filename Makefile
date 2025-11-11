.PHONY: install dev test lint format

# Install project + dev dependencies (run this inside your virtualenv)
install:
	python -m pip install --upgrade pip
	pip install -e ".[dev]"

# Run the API locally (expects .env and a virtualenv already activated)
dev:
	uvicorn app.main:app --reload

# Run tests
test:
	pytest -q

# Lint (no changes, just checks)
lint:
	ruff check .
	black --check .

# Auto-format & fix lintable issues
format:
	black .
	ruff check . --fix