dev:
	curl https://raw.githubusercontent.com/scottleechua/data/main/spam-and-marketing-sms/text-messages.csv > text-messages.csv
	poetry run python app.py

setup:
	poetry install
	poetry run pre-commit install