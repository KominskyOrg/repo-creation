PIP := $(shell command -v pip 2> /dev/null)
PIPENV := $(shell command -v pipenv 2> /dev/null)
PYTEST := pipenv run pytest tests
PYTHON := pipenv run python src/terraform_creation.py

.PHONY: setup
setup: $(PIP)
ifndef PIP
	$(error "pip is not available, please install pip")
endif
ifndef PIPENV
	pip install pipenv
endif
	pipenv sync --dev

.PHONY: test
test: setup
	$(PYTEST)

.PHONY: run
run: setup
	$(PYTHON)