.PHONY: dev init release update

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

release:
	./update-robots.zsh && \
	if ! git diff --quiet; then \
		git add . && \
		git commit -m "Update files before version bump"; \
	fi && \
	uv version --bump minor && \
	VERSION=$$(uv run python -c "import re; print(re.search(r'version = \"([^\"]+)\"', open('pyproject.toml').read()).group(1))") && \
	git add pyproject.toml uv.lock && \
	git commit -m "Bump version to $$VERSION" && \
	git tag -a "v$$VERSION" -m "Version $$VERSION" && \
	git push && git push --tags