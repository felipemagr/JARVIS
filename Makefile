SHELL := /usr/bin/env bash
DOCKER_COMMAND_FLAG := $(shell which docker 2> /dev/null)
PROJECT_NAME := $(shell poetry version | awk {'print $$1'})
PROJECT_VERSION := $(shell poetry version | awk {'print $$2'})
PIP_CMD := $(shell command -v pip || echo "")
PIP3_CMD := $(shell command -v pip3 || echo "")
POETRY_VERSION := 1.8.5

ifeq ($(PIP_CMD),)
	PIP_COMMAND_FLAG = pip3
else
	PIP_COMMAND_FLAG = pip
endif

ifeq ($(shell which podman 2> /dev/null),)
	ifneq ($(shell which docker 2> /dev/null),)
		DOCKER_COMMAND_FLAG := docker
	endif
else
	DOCKER_COMMAND_FLAG := podman
endif

.DEFAULT_GOAL := help

.PHONY: build
build: download-poetry install  ## Build the project.

.PHONY: clean
clean:  ## Clean unused files.
	@find ./ -name '*.pyc' -o -name '__pycache__' -o -name 'Thumbs.db' -o -name '*~' -exec rm -rf {} +;
	@rm -rf .cache .pytest_cache .mypy_cache build dist *.egg-info htmlcov .tox/ docs/_build
	@echo "Project cleaned."

.PHONY: test
test:  ## Run tests and generate coverage report.
	@export GENAI_ENVIRONMENT=test && \
	poetry run coverage run -m pytest --junitxml=xunit-result.xml   && \
	poetry run coverage report  && \
	poetry run coverage xml

.PHONY: download-poetry
download-poetry:  ## Download poetry
	@echo "Installing poetry ${POETRY_VERSION}..."
	@$(PIP_COMMAND_FLAG) install poetry==${POETRY_VERSION}
	@echo "Poetry installed at: $$(which poetry)"

.PHONY: help
help:  ## Show this help.
	@echo "Use: make <target>"
	@echo ""
	@echo "Targets available:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install:  ## Install the project in dev mode.
	poetry install
	@echo "Don't forget to run 'make shell' if you got errors."

.PHONY: run-black
run-black:  ## Run black to format code.
	@echo "Running black to format code... 🪄"
	@poetry run black .

.PHONY: run-flake8
run-flake8:  ## Run flake8 to revision code format.
	@echo "Running flake8 to revision code format... 🪄"
	@poetry run flake8 --config pyproject.toml

.PHONY: run-isort
run-isort:  ## Run isort to organize imports.
	@echo "Running isort to organize imports... 🪄"
	@poetry run isort .

.PHONY: run-pautoflake
run-pautoflake:  ## Run pautoflake to delete unused imports.
	@echo "Running pautoflake to delete unused imports... 🪄"
	@poetry run pautoflake --config pyproject.toml ./src ./tests

.PHONY: shell
shell:  ## Open a virtual environment.
	poetry shell
