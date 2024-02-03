from pathlib import Path
import typer
from rich import print
from kedro_inspect.core import KedroProject


def main():
    project_path = "demo-project"
    project_path = Path(project_path).resolve()
    project = KedroProject(project_path)
    unused_datasets = project.find_unused_datasets()
    typer.echo(unused_datasets)


# Direct Usage
# Implicit Usage (dictionary)
#