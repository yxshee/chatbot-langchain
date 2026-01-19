.PHONY: install lint format test run docker-build docker-run help

help:
	@echo "Available commands:"
	@echo "  install      Install dependencies"
	@echo "  lint         Run linters (ruff, mypy)"
	@echo "  format       Run formatters (ruff)"
	@echo "  test         Run tests (pytest)"
	@echo "  run          Run the Streamlit app"
	@echo "  docker-build Build the Docker image"
	@echo "  docker-run   Run the Docker container"

install:
	pip install -r requirements.txt
	pip install ruff mypy pytest

lint:
	ruff check .
	mypy src

format:
	ruff check --fix .
	ruff format .

test:
	pytest

run:
	streamlit run streamlit_app.py

docker-build:
	docker build -t rbi-bot .

docker-run:
	docker run -p 8501:8501 --env-file .env rbi-bot
