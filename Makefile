PIP := $(shell command -v pip 2> /dev/null)
PIPENV := $(shell command -v pipenv 2> /dev/null)
PYTEST := pipenv run pytest tests
PYTHON := pipenv run python src/terraform_creation.py

DIR = tf
VAR_FILE = secret.tfvars

define terraform_command
	@if [ -z "$(1)" ]; then \
		echo "Please specify a directory using DIR=<directory>"; \
	elif [ ! -d "$(1)" ]; then \
		echo "Directory $(1) does not exist."; \
	else \
		terraform -chdir=$(1) $(2); \
	fi
endef


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

.PHONY: setup_tf
setup_tf:
	$(call terraform_command,$(DIR),init)

.PHONY: apply
apply:
	$(call terraform_command,$(DIR),apply -var-file=$(VAR_FILE))

.PHONY: plan
plan:
	$(call terraform_command,$(DIR),plan -var-file=$(VAR_FILE))