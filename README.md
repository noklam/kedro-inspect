# kedro-inspect

## Install

``` sh
pip install kedro-inspect
```


## How to use

To see what commands are available, run:
```
kedro-inspect
```

Run this command to compile configurations to files:
```
kedro-inspect compile
```
This will compile all configurations to a separate `compile` folder.


## Todo
- Implemented a TraceHook that can be included in project without calling CLI

# Stack
Dependency: pdm
Docs: mkdocs
CLI: typer

Todo:
- Config Tracibility - is it possible to trace where's the config coming from (useful for VSCode extension)
