setup:
	pip install pipenv
	pipenv sync --dev

test: setup
	pipenv run pytest tests

run: setup
	pipenv run python src/terraform_creation.py