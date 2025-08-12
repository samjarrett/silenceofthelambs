FILES := silenceofthelambs tests setup.py

lint:
	uv run pylint ${FILES}
	uv run black --check ${FILES}
	uv run isort ${FILES} --check-only

test:
	uv run pytest --cov silenceofthelambs
	uv run mypy silenceofthelambs

fix:
	uv run black ${FILES}
	uv run isort ${FILES}
	$(MAKE) lint
