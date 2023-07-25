setup:
	pipenv install

apply:
	cd tf && terraform apply -var-file=secret.tfvars

plan:
	cd tf && terraform plan -var-file=secret.tfvars

test: setup
	pipenv run pytest tests/test_repo_config_parser.py

run: setup
	pipenv run python src/terraform_creation.py