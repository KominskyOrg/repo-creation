import os
import json
import tempfile
from src.terraform_creation import generate_all_terraform_files
from src.config_parser import load_json_config, generate_repo_block, parse_json_config


def test_generate_all_terraform_files(tmpdir):
    # Create a temporary directory for the test
    temp_dir = tmpdir.mkdir("test_configs")
    test_file_content = {
        "name": "test-repo",
        "description": "Test repository",
        "has_issues": True,
    }

    # Write test data to a JSON file in the temporary directory
    with open(os.path.join(temp_dir, "test.json"), "w") as f:
        json.dump(test_file_content, f)

    # Run the function to generate Terraform files
    generate_all_terraform_files(str(temp_dir))

    # Verify that the Terraform file was created
    assert os.path.exists(os.path.join(temp_dir.dirname, "tf", "test.tf"))


def test_load_json_config():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp:
        json.dump({"test": "data"}, temp)
        temp.flush()
        data = load_json_config(temp.name)
        assert data == {"test": "data"}
        os.unlink(temp.name)


def test_generate_repo_block():
    repo_config = {
        "name": "test-repo",
        "description": "Test repository",
        "has_issues": True,
        "branch_protections": {
            "branch": "main",
            "enforce_admins": False,
            "required_status_checks": {"strict": False, "contexts": []},
            "required_pull_request_reviews": {
                "dismiss_stale_reviews": False,
                "dismissal_users": [],
                "dismissal_teams": [],
                "require_code_owner_reviews": False,
            },
        },
    }
    result = generate_repo_block(repo_config)
    assert 'resource "github_repository" "test-repo"' in result
    assert 'name        = "test-repo"' in result
    assert 'description = "Test repository"' in result
    assert "has_issues = true" in result
    assert 'resource "github_branch_protection_v3" "test-repo-protection"' in result
    assert f'resource "github_branch" "{repo_config["name"]}_main"' in result
    assert f'resource "github_branch_default" "{repo_config["name"]}_default"' in result


def test_parse_json_config():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp:
        json.dump(
            {"name": "test-repo", "description": "Test repository", "has_issues": True},
            temp,
        )
        temp.flush()
        result = parse_json_config(temp.name)
        assert 'resource "github_repository" "test-repo"' in result
        os.unlink(temp.name)
