.PHONY: dev init

dev:
	curl https://raw.githubusercontent.com/scottleechua/data/main/spam-and-marketing-sms/text-messages.csv > text-messages.csv
	poetry run python app.py

init:
	poetry install --with dev
	poetry run pre-commit install