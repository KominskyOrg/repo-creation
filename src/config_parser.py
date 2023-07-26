import json


def load_json_config(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data


def generate_repo_block(repo_config):
    terraform_block = f'resource "github_repository" "{repo_config["name"]}" {{\n'
    terraform_block += f'  name        = "{repo_config["name"]}"\n'
    terraform_block += f'  description = "{repo_config.get("description", "")}"\n'
    terraform_block += f'  visibility  = "{repo_config.get("visibility", "private")}"\n'

    optional_attributes = [
        "homepage_url",
        "has_issues",
        "has_projects",
        "has_wiki",
        "is_template",
        "allow_merge_commit",
        "allow_rebase_merge",
        "allow_squash_merge",
        "delete_branch_on_merge",
        "archived",
        "topics",
        "vulnerability_alerts",
        "automated_security_fixes",
        "license_template",
        "gitignore_template",
    ]

    for attribute in optional_attributes:
        if attribute in repo_config:
            if isinstance(repo_config[attribute], bool):
                terraform_block += (
                    f"  {attribute} = {str(repo_config[attribute]).lower()}\n"
                )
            else:
                terraform_block += f'  {attribute} = "{repo_config[attribute]}"\n'

    terraform_block += "}\n\n"

    # Add branch protection if it's specified in the config
    if "branch_protections" in repo_config:
        protection_config = repo_config["branch_protections"]
        terraform_block += f'resource "github_branch_protection_v3" "{repo_config["name"]}-protection" {{\n'
        terraform_block += (
            f'  depends_on  = [github_branch_default.{repo_config["name"]}_default]\n'
        )
        terraform_block += (
            f'  repository = github_repository.{repo_config["name"]}.name\n'
        )
        terraform_block += (
            f'  branch       = "{protection_config.get("branch", "main")}"\n'
        )
        terraform_block += f'  enforce_admins = {str(protection_config.get("enforce_admins", False)).lower()}\n'

        if "required_status_checks" in protection_config:
            checks_config = protection_config["required_status_checks"]
            terraform_block += "  required_status_checks {\n"
            terraform_block += (
                f'    strict   = {str(checks_config.get("strict", False)).lower()}\n'
            )
            terraform_block += (
                f'    checks = {json.dumps(checks_config.get("contexts", []))}\n'
            )
            terraform_block += "  }\n"

        if "required_pull_request_reviews" in protection_config:
            reviews_config = protection_config["required_pull_request_reviews"]
            terraform_block += "  required_pull_request_reviews {\n"
            terraform_block += f'    dismiss_stale_reviews = {str(reviews_config.get("dismiss_stale_reviews", False)).lower()}\n'
            terraform_block += f'    dismissal_users = {json.dumps(reviews_config.get("dismissal_users", []))}\n'
            terraform_block += f'    dismissal_teams = {json.dumps(reviews_config.get("dismissal_teams", []))}\n'
            terraform_block += f'    require_code_owner_reviews = {str(reviews_config.get("require_code_owner_reviews", False)).lower()}\n'
            terraform_block += "  }\n"

        terraform_block += "}\n"
    terraform_block += generate_branch_and_default_block(repo_config["name"])
    return terraform_block


def generate_branch_and_default_block(repo_name):
    return f"""
resource "github_branch" "{repo_name}_main" {{
  repository = github_repository.{repo_name}.name
  branch     = "main"
}}

resource "github_branch_default" "{repo_name}_default" {{
  repository = github_repository.{repo_name}.name
  branch     = github_branch.{repo_name}_main.branch
}}
"""


def parse_json_config(file_path):
    data = load_json_config(file_path)
    # Wrap in list if data is a dictionary
    if isinstance(data, dict):
        data = [data]
    main_tf_content = ""
    for repo_config in data:
        repo_block = generate_repo_block(repo_config)
        main_tf_content += repo_block
    return main_tf_content


# Example usage:
# parse_json_config('config.json')
