install:
	pip install -e ".[dev]"

preview:
	mkdocs serve

build-docs:
	mkdocs build