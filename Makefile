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

.PHONY: docker-build
docker-build:  ## Build the docker image.
	@export GENAI_ENVIRONMENT=local;
	$(DOCKER_COMMAND_FLAG) build \
		--platform linux/amd64 \
		--build-arg GENAI_ENVIRONMENT=$(GENAI_ENVIRONMENT) \
		-t $(PROJECT_NAME):$(PROJECT_VERSION) .

.PHONY: docker-run
docker-run:  ## Run the docker image.
	-$(DOCKER_COMMAND_FLAG) network create jarvis-net
	$(DOCKER_COMMAND_FLAG) run --rm --platform linux/amd64 \
		--env-file .env \
		-p 8000:8000 \
		--network=jarvis-net \
		--name $(PROJECT_NAME) \
		$(PROJECT_NAME):$(PROJECT_VERSION)

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

.PHONY: shell
shell:  ## Open a virtual environment.
	poetry shell
