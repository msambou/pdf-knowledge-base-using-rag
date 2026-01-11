# Dev Instructions

This is a FastAPI application where poetry is used as dependency management.

## Creating a new poetry project

    poetry new rag_app # Note that a new virtual environment will be created after this command is run

    poetry install

## Checking the virtual environment

    poetry env info # This gives info about the current virtual environment in use

    poetry env list # Shows the list of virtual environments

    poetry env use python3.14 # Add a new virtual environment

    poetry env remove python3.6 # Remove a virtual environment


## Dependency Management
Dependencies are managed using the pyproject.toml file.
After adding a new dependency, run `poetry update` to install them.

## Running the App

    poetry run uvicorn app.app:app --reload
