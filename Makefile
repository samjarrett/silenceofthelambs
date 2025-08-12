FILES := silenceofthelambs tests

lint:
	pylint ${FILES}
	black --check ${FILES}
	isort ${FILES} --check-only

test:
	pytest --cov silenceofthelambs
	mypy silenceofthelambs

fix:
	black ${FILES}
	isort ${FILES}
	$(MAKE) lint
