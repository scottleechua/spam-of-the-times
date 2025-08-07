.PHONY: dev init

dev:
	curl https://raw.githubusercontent.com/scottleechua/data/main/spam-and-marketing-sms/text-messages.csv > text-messages.csv
	uv run python app.py

init:
	uv pip install -r requirements.txt -r requirements-dev.txt
	uv run pre-commit install