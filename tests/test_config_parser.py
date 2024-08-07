import json
from src.config_parser import (
    load_json_config,
    generate_optional_attributes,
    generate_required_status_checks_block,
    generate_required_pull_request_reviews_block,
    generate_restrictions_block,
    parse_json_config,
    generate_github_branch_protection_v3_block,
    generate_github_repository_block,
    generate_github_branch_block,
    generate_github_branch_default_block,
    parse_json_config,
)

def test_generate_github_branch_protection_v3_block():
    protection_config = {
        "name": "test-repo",
        "branch": "main",
        "enforce_admins": True,
        "require_signed_commits": True,
        "requires_approving_reviews": 2,
        "requires_code_owner_reviews": True,
        "requires_commit_signatures": False,
        "allows_deletions": False,
        "allows_force_pushes": False
    }
    
    result = generate_github_branch_protection_v3_block(protection_config)
    
    expected_result = '''resource "github_branch_protection_v3" "test-repo-protection" {
  depends_on  = [github_branch_default.test-repo_default]
  repository = github_repository.test-repo.name
  branch       = "main"
  enforce_admins = true
  require_signed_commits = true
  requires_approving_reviews = "2"
  requires_code_owner_reviews = true
  requires_commit_signatures = false
  allows_deletions = false
  allows_force_pushes = false
}
'''
    
    assert result == expected_result


def test_load_json_config():
    with open("tests/test_config.json", "w") as f:
        json.dump({"key": "value"}, f)

    result = load_json_config("tests/test_config.json")
    assert result == {"key": "value"}


def test_generate_optional_attributes():
    resource_config = {
        "attribute1": "value1",
        "attribute2": True,
        "attribute3": "value3",
    }
    optional_attributes = ["attribute1", "attribute2"]
    result = generate_optional_attributes(resource_config, optional_attributes)
    expected_result = '  attribute1 = "value1"\n  attribute2 = true\n'
    assert result == expected_result


def test_generate_required_status_checks_block():
    checks_config = {
        "required_status_checks": {"strict": True, "contexts": ["check1", "check2"]}
    }
    result = generate_required_status_checks_block(checks_config)
    expected_result = '''  required_status_checks {
  strict = true
  contexts = ["check1", "check2"]
  }
'''
    assert result == expected_result


def test_generate_required_pull_request_reviews_block():
    reviews_config = {
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": True,
            "dismissal_users": ["user1", "user2"],
            "require_code_owner_reviews": True,
        }
    }
    result = generate_required_pull_request_reviews_block(reviews_config)
    expected_result = '''  required_pull_request_reviews {
  dismiss_stale_reviews = true
  dismissal_users = ["user1", "user2"]
  dismissal_teams = ["team1", "team2"]
  require_code_owner_reviews = true
  }
'''
    assert result == expected_result


def test_generate_restrictions_block():
    restrictions_config = {
        "restrictions": {"users": ["user1", "user2"], "teams": ["team1", "team2"]}
    }
    result = generate_restrictions_block(restrictions_config)
    expected_result = '''  restrictions {
  users = ["user1", "user2"]
  teams = ["team1", "team2"]
  }
'''
    assert result == expected_result


def test_parse_json_config():
    with open("tests/test_config.json", "w") as f:
        json.dump([{"name": "test_repo"}], f)

    result = parse_json_config("tests/test_config.json")
    assert 'resource "github_repository" "test_repo"' in result


def test_generate_github_repository_block():
    repo_config = {
        "name": "test-repo",
        "description": "Test repository",
        "visibility": "public",
        "auto_init": "true",
        "homepage_url": "https://example.com",
        "has_issues": True,
        "has_projects": False,
        "has_wiki": True,
        "is_template": False,
        "allow_merge_commit": True,
        "allow_rebase_merge": False,
        "allow_squash_merge": True,
        "delete_branch_on_merge": False,
        "archived": False,
        "topics": ["test", "example"],
        "vulnerability_alerts": True,
        "license_template": "mit",
        "gitignore_template": "Python"
    }
    
    result = generate_github_repository_block(repo_config)
    expected_result = '''resource "github_repository" "test-repo" {
  name        = "test-repo"
  description = "Test repository"
  visibility  = "public"
  auto_init   = "true"
  homepage_url = "https://example.com"
  has_issues = true
  has_projects = false
  has_wiki = true
  is_template = false
  allow_merge_commit = true
  allow_rebase_merge = false
  allow_squash_merge = true
  delete_branch_on_merge = false
  archived = false
  topics = ["test", "example"]
  vulnerability_alerts = true
  license_template = "mit"
  gitignore_template = "Python"
}
'''
    assert result == expected_result


def test_generate_github_branch_block():
    branch_config = {
        "name": "test-repo",
        "branch": "develop"
    }
    
    result = generate_github_branch_block(branch_config)
    expected_result = '''resource "github_branch" "test-repo_main" {
  repository = github_repository.test-repo.name
  branch     = "develop"
}
'''
    assert result == expected_result


def test_generate_github_branch_default_block():
    default_config = {
        "name": "test-repo"
    }
    
    result = generate_github_branch_default_block(default_config)
    expected_result = '''resource "github_branch_default" "test-repo_default" {
  repository = github_repository.test-repo.name
  branch     = github_branch.test-repo_main.branch
}
'''
    assert result == expected_result


def test_parse_json_config_with_single_repo():
    with open("tests/test_single_repo_config.json", "w") as f:
        json.dump({
            "name": "test-repo",
            "description": "Test repository",
            "visibility": "public"
        }, f)
    
    result = parse_json_config("tests/test_single_repo_config.json")
    assert 'resource "github_repository" "test-repo"' in result
    assert 'resource "github_branch" "test-repo_main"' in result
    assert 'resource "github_branch_default" "test-repo_default"' in result
    assert 'resource "github_branch_protection_v3" "test-repo-protection"' in result


def test_parse_json_config_with_multiple_repos():
    with open("tests/test_multiple_repos_config.json", "w") as f:
        json.dump([
            {
                "name": "repo1",
                "description": "Repository 1",
                "visibility": "public"
            },
            {
                "name": "repo2",
                "description": "Repository 2",
                "visibility": "private"
            }
        ], f)
    
    result = parse_json_config("tests/test_multiple_repos_config.json")
    assert 'resource "github_repository" "repo1"' in result
    assert 'resource "github_repository" "repo2"' in result
    assert 'resource "github_branch" "repo1_main"' in result
    assert 'resource "github_branch" "repo2_main"' in result
    assert 'resource "github_branch_default" "repo1_default"' in result
    assert 'resource "github_branch_default" "repo2_default"' in result
    assert 'resource "github_branch_protection_v3" "repo1-protection"' in result
    assert 'resource "github_branch_protection_v3" "repo2-protection"' in result


def test_generate_required_status_checks_block():
    checks_config = {
        "required_status_checks": {
            "strict": True,
            "contexts": ["ci/test", "security/scan"]
        }
    }
    
    result = generate_required_status_checks_block(checks_config)
    expected_result = '''  required_status_checks {
  strict = true
  contexts = ["ci/test", "security/scan"]
  }
'''
    assert result == expected_result


def test_generate_required_status_checks_block_empty():
    checks_config = {}
    
    result = generate_required_status_checks_block(checks_config)
    assert result == ""


def test_generate_required_pull_request_reviews_block():
    reviews_config = {
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": True,
            "dismissal_users": ["user1", "user2"],
            "dismissal_teams": ["team1", "team2"],
            "require_code_owner_reviews": True
        }
    }
    
    result = generate_required_pull_request_reviews_block(reviews_config)
    expected_result = '''  required_pull_request_reviews {
  dismiss_stale_reviews = true
  dismissal_users = ["user1", "user2"]
  dismissal_teams = ["team1", "team2"]
  require_code_owner_reviews = true
  }
'''
    assert result == expected_result


def test_generate_required_pull_request_reviews_block_empty():
    reviews_config = {}
    
    result = generate_required_pull_request_reviews_block(reviews_config)
    assert result == ""


def test_generate_restrictions_block():
    restrictions_config = {
        "restrictions": {
            "users": ["user1", "user2"],
            "teams": ["team1", "team2"]
        }
    }
    
    result = generate_restrictions_block(restrictions_config)
    expected_result = '''  restrictions {
  users = ["user1", "user2"]
  teams = ["team1", "team2"]
  }
'''
    assert result == expected_result


def test_generate_restrictions_block_empty():
    restrictions_config = {}
    
    result = generate_restrictions_block(restrictions_config)
    assert result == ""
