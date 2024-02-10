from pathlib import Path
import typer
from kedro_inspect.core import KedroProject

app = typer.Typer()
# compile_app = typer.Typer()
# app.add_typer(compile_app, name="compile", help="Compile configurations.")
@app.command()
def datasets():
    project_path = "demo-project"
    project_path = Path(project_path).resolve()
    project = KedroProject(project_path)
    unused_datasets = project.find_unused_datasets()
    typer.echo(unused_datasets)

@app.command()
def compile():
    print("Compile")
    ...
# Direct Usage
# Implicit Usage (dictionary)
#
if __name__ == "__main__":
    app()