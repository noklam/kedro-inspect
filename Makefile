install:
	pip install -e ".[dev]"

preview:
	mkdocs serve

build-docs:
	mkdocs build

test:
	cd demo-project & kedro-inspect