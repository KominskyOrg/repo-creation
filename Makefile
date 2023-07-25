apply:
	cd tf && terraform apply -var-file=secret.tfvars

plan:
	cd tf && terraform plan -var-file=secret.tfvars

test:
	pytest tests/test_repo_config_parser.py

run:
	python repo-creation/terraform_creation.py