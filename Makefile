install:
	pip install -e ".[dev]"

preview:
	mkdocs serve

build-docs:
	mkdocs build

test:
	cd demo-project && kedro-inspect

lint:
	pre-commit run -a --hook-stage manual

run:
	cd demo-project && kedro run --runner=kedro_inspect.runner.DryRunner
