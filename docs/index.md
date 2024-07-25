<!-- # Welcome to MkDocs

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files. -->

# Welcome to kedro-inspect!
This is a lightweight toolkit that provides a CLI and Python API to inspect your Kedro Project

## Why do you need this
Have you ever pick up a big kedro project where you have no idea how things work?
1. Are there unused parameters and datasets?
2. Which pipeline is using this dataset?
3. Where is this configuration coming from?
4. Which dataset factory pattern is not used at all?
5. Which pattern is this dataset using?
6. Which node used this dataset as input/outputs?

## Unused Parameters
There are few types of parameters
1. Directly used parameters
2. Implicit used parameters, which the value is a dictionary
3. Unused parameters, parameters that are defined but never used anywhere (You should remove it!)

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