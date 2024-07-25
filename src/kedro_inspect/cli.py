from pathlib import Path

import typer
import yaml

from kedro_inspect.core import KedroProject

app = typer.Typer(no_args_is_help=True)
# compile_app = typer.Typer()
# app.add_typer(compile_app, name="compile", help="Compile configurations.")


def create_project():
    project_path = Path("")
    project_path = Path(project_path).resolve()
    project = KedroProject(project_path)
    return project


@app.command()
def datasets():
    project = create_project()
    unused_datasets = project.find_unused_datasets()
    typer.echo(unused_datasets)


@app.command()
def compile():
    project = create_project()
    config_loader = project.config_loader
    keys = config_loader.config_patterns.keys()
    compiled_config = {}

    def write_yaml(config: dict, key):
        path = Path("compile")
        path.mkdir(exist_ok=True, parents=True)
        write_path = path / f"{key}.yml"
        # TODO: Should write to CONF_SOURCE/compiled instead.
        with open(write_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            print(f"Files written to {str(write_path.resolve().absolute())}")

    for config_key in keys:
        compiled = config_loader[config_key]
        compiled_config[config_key] = compiled
        write_yaml(compiled, config_key)
        # DryRunner


    # For `catalog` only
    # for ds_name, ds_config in catalog.items():
    #     ds_config = _resolve_credentials(  # noqa: PLW2901
    #         ds_config, credentials
    #     )
    #     if cls._is_pattern(ds_name):
    #         # Add each factory to the dataset_patterns dict.
    #         dataset_patterns[ds_name] = ds_config

    #     else:
    #         datasets[ds_name] = AbstractDataset.from_config(
    #             ds_name, ds_config, load_versions.get(ds_name), save_version
    #         )

    # it is not iterable
    #     print(config_group)
    ...


# Direct Usage
# Implicit Usage (dictionary)
#
if __name__ == "__main__":
    app()
