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
                attributes_block += f'  {attribute} = {str(resource_config[attribute]).lower()}\n'
            elif isinstance(resource_config[attribute], list):
                if all(isinstance(item, str) for item in resource_config[attribute]):
                    # Maintain list format with double quotes
                    list_values = ", ".join(f'"{item}"' for item in resource_config[attribute])
                else:
                    list_values = ", ".join(str(item) for item in resource_config[attribute])
                attributes_block += f"  {attribute} = [{list_values}]\n"
            else:
                attributes_block += f'  {attribute} = "{resource_config[attribute]}"\n'
    return attributes_block

# Function to generate github_repository block
def generate_github_repository_block(repo_config):
    # Main attributes
    repo_block = f"""resource "github_repository" "{repo_config["name"]}" {{
  name                 = "{repo_config["name"]}"
  description          = "{repo_config.get("description", "")}"
  visibility           = "{repo_config.get("visibility", "private")}"
  gitignore_template   = "{repo_config.get("gitignore_template", "")}"
  allow_merge_commit   = {str(repo_config.get("allow_merge_commit", False)).lower()}
  allow_squash_merge   = {str(repo_config.get("allow_squash_merge", True)).lower()}
  allow_rebase_merge   = {str(repo_config.get("allow_rebase_merge", False)).lower()}
  delete_branch_on_merge = {str(repo_config.get("delete_branch_on_merge", False)).lower()}
  archived             = {str(repo_config.get("archived", False)).lower()}
"""

    # Optional attributes (excluding those already set above)
    optional_attributes = [
        "homepage_url",
        "has_issues",
        "has_projects",
        "has_wiki",
        "is_template",
        "topics",
        "vulnerability_alerts",
        "license_template",
    ]
    repo_block += generate_optional_attributes(repo_config, optional_attributes)

    # Close the resource block
    repo_block += "}\n\n"

    return repo_block

# Function to generate github_repository_collaborator blocks
def generate_github_repository_collaborators_block(repo_config):
    collaborators = repo_config.get("collaborators", [])
    collaborators_block = ""
    for collaborator in collaborators:
        collaborators_block += f"""resource "github_repository_collaborator" "{repo_config["name"]}_{collaborator["username"]}_collaborator" {{
  repository = github_repository.{repo_config["name"]}.name
  username   = "{collaborator["username"]}"
  permission = "{collaborator.get("permission", "push")}"
}}

"""
    return collaborators_block

# Function to generate github_branch block
def generate_github_branch_block(repo_name, branch_config):
    # Unique resource name by including repo name
    branch_resource_name = f"{repo_name}_{branch_config['name']}_branch"
    branch_block = f"""resource "github_branch" "{branch_resource_name}" {{
  repository = github_repository.{repo_name}.name
  branch     = "{branch_config.get("branch", "main")}"
}}

"""
    return branch_block

# Function to generate github_branch_default block
def generate_github_branch_default_block(repo_name, branch_config):
    if not branch_config.get("is_default", False):
        return ""
    # Unique resource name
    default_resource_name = f"{repo_name}_{branch_config['name']}_default"
    default_block = f"""resource "github_branch_default" "{default_resource_name}" {{
  repository = github_repository.{repo_name}.name
  branch     = github_branch.{repo_name}_{branch_config['name']}_branch.branch
}}

"""
    return default_block

# Function to generate github_branch_protection_v3 block
def generate_github_branch_protection_v3_block(repo_name, branch_config):
    protection = branch_config.get("protection", {})
    if not protection:
        return ""

    # Unique resource name
    protection_resource_name = f"{repo_name}_{branch_config['name']}_protection"

    protection_block = f"""resource "github_branch_protection_v3" "{protection_resource_name}" {{
  repository            = github_repository.{repo_name}.name
  branch                = github_branch.{repo_name}_{branch_config['name']}_branch.branch
  enforce_admins        = {str(protection.get("enforce_admins", False)).lower()}
  require_signed_commits = {str(protection.get("require_signed_commits", False)).lower()}
  requires_approving_reviews = {str(protection.get("requires_approving_reviews", False)).lower()}
  requires_code_owner_reviews = {str(protection.get("requires_code_owner_reviews", False)).lower()}
  requires_commit_signatures = {str(protection.get("requires_commit_signatures", False)).lower()}
  allows_deletions       = {str(protection.get("allows_deletions", False)).lower()}
  allows_force_pushes    = {str(protection.get("allows_force_pushes", False)).lower()}
"""

    # Optional attributes (excluding those already set above)
    optional_attributes = [
        # Already included above
    ]
    protection_block += generate_optional_attributes(protection, optional_attributes)

    # Nested blocks
    protection_block += generate_required_status_checks_block(protection)
    protection_block += generate_required_pull_request_reviews_block(protection)
    protection_block += generate_restrictions_block(protection)

    # Close the resource block
    protection_block += "}\n\n"

    return protection_block

# Function to generate required_status_checks block
def generate_required_status_checks_block(checks_config):
    if "required_status_checks" not in checks_config:
        return ""
    checks = checks_config["required_status_checks"]
    if not checks:
        return ""
    checks_block = "  required_status_checks {\n"

    # Optional attributes
    optional_attributes = [
        "strict",
        "contexts",
    ]
    checks_block += generate_optional_attributes(checks, optional_attributes)

    checks_block += "  }\n"
    return checks_block

# Function to generate required_pull_request_reviews block
def generate_required_pull_request_reviews_block(reviews_config):
    if "required_pull_request_reviews" not in reviews_config:
        return ""
    reviews = reviews_config["required_pull_request_reviews"]
    if not reviews:
        return ""
    reviews_block = "  required_pull_request_reviews {\n"

    # Optional attributes
    optional_attributes = [
        "dismiss_stale_reviews",
        "dismissal_users",
        "dismissal_teams",
        "require_code_owner_reviews",
    ]
    reviews_block += generate_optional_attributes(reviews, optional_attributes)

    reviews_block += "  }\n"
    return reviews_block

# Function to generate restrictions block
def generate_restrictions_block(restrictions_config):
    if "restrictions" not in restrictions_config:
        return ""
    restrictions = restrictions_config["restrictions"]
    if not restrictions:
        return ""
    restrictions_block = "  restrictions {\n"

    # Optional attributes
    optional_attributes = [
        "users",
        "teams",
    ]
    restrictions_block += generate_optional_attributes(restrictions, optional_attributes)

    restrictions_block += "  }\n"
    return restrictions_block

def parse_json_config(file_path):
    data = load_json_config(file_path)
    # Wrap in list if data is a dictionary
    if isinstance(data, dict):
        data = [data]
    main_tf_content = ""
    for repo_config in data:
        repo_name = repo_config["name"]

        # Generate repository block
        repo_block = generate_github_repository_block(repo_config)
        main_tf_content += repo_block

        # Generate collaborators block
        collaborators_block = generate_github_repository_collaborators_block(repo_config)
        main_tf_content += collaborators_block

        # Iterate over branches
        branches = repo_config.get("branches", [])
        for branch in branches:
            branch_block = generate_github_branch_block(repo_name, branch)
            main_tf_content += branch_block

            default_block = generate_github_branch_default_block(repo_name, branch)
            if default_block:
                main_tf_content += default_block

            protection_block = generate_github_branch_protection_v3_block(repo_name, branch)
            if protection_block:
                main_tf_content += protection_block

    return main_tf_content
