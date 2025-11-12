.PHONY: dev init update

dev:
	curl https://raw.githubusercontent.com/scottleechua/data/main/spam-and-marketing-sms/text-messages.csv > text-messages.csv
	uv run python app.py

init:
	uv pip install -e ".[dev]"
	uv run pre-commit install

update:
	uv lock --upgrade
	uv export --format requirements-txt -o requirements.txt
	uv export --format requirements-txt --extra dev -o requirements-dev.txt