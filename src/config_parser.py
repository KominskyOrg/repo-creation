import json


def load_json_config(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data


# Helper function to generate optional attributes
def generate_optional_attributes(resource_config, optional_attributes):
    attributes_block = ""
    for attribute in optional_attributes:
        if attribute in resource_config:
            if isinstance(resource_config[attribute], bool):
                attributes_block += (
                    f"  {attribute} = {str(resource_config[attribute]).lower()}\n"
                )
            elif isinstance(resource_config[attribute], list):
                # Maintain list format with double quotes
                list_values = ", ".join(
                    f'"{item}"' for item in resource_config[attribute]
                )
                attributes_block += f"  {attribute} = [{list_values}]\n"
            else:
                attributes_block += f'  {attribute} = "{resource_config[attribute]}"\n'
    return attributes_block


# Function to generate github_repository block
def generate_github_repository_block(repo_config):
    # Main attributes
    repo_block = f"""resource "github_repository" "{repo_config["name"]}" {{
  name        = "{repo_config["name"]}"
  description = "{repo_config.get("description", "")}"
  visibility  = "{repo_config.get("visibility", "private")}"\n"""

    # Optional attributes
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
        "license_template",
        "gitignore_template",
    ]
    repo_block += generate_optional_attributes(repo_config, optional_attributes)

    repo_block += "}\n"

    return repo_block


# Function to generate github_branch block
def generate_github_branch_block(branch_config):
    # Main attributes
    branch_block = f"""resource "github_branch" "{branch_config["name"]}_main" {{
  repository = github_repository.{branch_config["name"]}.name
  branch     = "{branch_config.get("branch", "main")}"\n"""

    # There are no optional attributes for this resource according to the docs

    branch_block += "}\n"

    return branch_block


# Function to generate github_branch_default block
def generate_github_branch_default_block(default_config):
    # Main attributes
    default_block = f"""resource "github_branch_default" "{default_config["name"]}_default" {{
  repository = github_repository.{default_config["name"]}.name
  branch     = github_branch.{default_config["name"]}_main.branch\n"""

    # There are no optional attributes for this resource according to the docs

    default_block += "}\n"

    return default_block


# Function to generate github_branch_protection_v3 block
def generate_github_branch_protection_v3_block(protection_config):
    # Main attributes
    protection_block = f"""resource "github_branch_protection_v3" "{protection_config["name"]}-protection" {{
  depends_on  = [github_branch_default.{protection_config["name"]}_default]
  repository = github_repository.{protection_config["name"]}.name
  branch       = "{protection_config.get("branch", "main")}"\n"""

    # Optional attributes
    optional_attributes = [
        "enforce_admins",
        "require_signed_commits",
        "requires_approving_reviews",
        "requires_code_owner_reviews",
        "requires_commit_signatures",
        "allows_deletions",
        "allows_force_pushes",
        # The following nested blocks will be handled separately
        # "required_status_checks",
        # "required_pull_request_reviews",
        # "restrictions",
    ]
    protection_block += generate_optional_attributes(
        protection_config, optional_attributes
    )

    # Nested blocks (to be added)
    # ...

    protection_block += "}\n"

    return protection_block


# Function to generate required_status_checks block
def generate_required_status_checks_block(checks_config):
    if "required_status_checks" not in checks_config:
        return ""
    checks_block = """  required_status_checks {\n"""

    # Optional attributes
    optional_attributes = [
        "strict",
        "checks",
    ]
    checks_block += generate_optional_attributes(
        checks_config["required_status_checks"], optional_attributes
    )

    checks_block += "  }\n"

    return checks_block


# Function to generate required_pull_request_reviews block
def generate_required_pull_request_reviews_block(reviews_config):
    if "required_pull_request_reviews" not in reviews_config:
        return ""
    reviews_block = """  required_pull_request_reviews {\n"""

    # Optional attributes
    optional_attributes = [
        "dismiss_stale_reviews",
        "dismissal_users",
        "dismissal_teams",
        "require_code_owner_reviews",
    ]
    reviews_block += generate_optional_attributes(
        reviews_config["required_pull_request_reviews"], optional_attributes
    )

    reviews_block += "  }\n"

    return reviews_block


# Function to generate restrictions block
def generate_restrictions_block(restrictions_config):
    if "restrictions" not in restrictions_config:
        return ""
    restrictions_block = """  restrictions {\n"""

    # Optional attributes
    optional_attributes = [
        "users",
        "teams",
    ]
    restrictions_block += generate_optional_attributes(
        restrictions_config["restrictions"], optional_attributes
    )

    restrictions_block += "  }\n"

    return restrictions_block


# Update the generate_github_branch_protection_v3_block function to include these nested blocks
def generate_github_branch_protection_v3_block(protection_config):
    # Main attributes
    protection_block = f"""resource "github_branch_protection_v3" "{protection_config["name"]}-protection" {{
  depends_on  = [github_branch_default.{protection_config["name"]}_default]
  repository = github_repository.{protection_config["name"]}.name
  branch       = "{protection_config.get("branch", "main")}"\n"""

    # Optional attributes
    optional_attributes = [
        "enforce_admins",
        "require_signed_commits",
        "requires_approving_reviews",
        "requires_code_owner_reviews",
        "requires_commit_signatures",
        "allows_deletions",
        "allows_force_pushes",
    ]
    protection_block += generate_optional_attributes(
        protection_config, optional_attributes
    )

    # Nested blocks
    protection_block += generate_required_status_checks_block(protection_config)
    protection_block += generate_required_pull_request_reviews_block(protection_config)
    protection_block += generate_restrictions_block(protection_config)

    protection_block += "}\n"

    return protection_block


def parse_json_config(file_path):
    data = load_json_config(file_path)
    # Wrap in list if data is a dictionary
    if isinstance(data, dict):
        data = [data]
    main_tf_content = ""
    for repo_config in data:
        # Generate blocks for each resource
        repo_block = generate_github_repository_block(repo_config)
        branch_block = generate_github_branch_block(repo_config)
        default_block = generate_github_branch_default_block(repo_config)
        protection_block = generate_github_branch_protection_v3_block(repo_config)

        # Combine all blocks
        main_tf_content += repo_block + branch_block + default_block + protection_block
    return main_tf_content


# Example usage:
# parse_json_config('config.json')
