import json
from src.config_parser import (
    load_json_config,
    generate_optional_attributes,
    generate_required_status_checks_block,
    generate_required_pull_request_reviews_block,
    generate_restrictions_block,
    parse_json_config,
)


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
        "required_status_checks": {"strict": True, "checks": ["check1", "check2"]}
    }
    result = generate_required_status_checks_block(checks_config)
    expected_result = '  required_status_checks {\n  strict = true\n  checks = ["check1", "check2"]\n  }\n'
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
    expected_result = '  required_pull_request_reviews {\n  dismiss_stale_reviews = true\n  dismissal_users = ["user1", "user2"]\n  require_code_owner_reviews = true\n  }\n'
    assert result == expected_result


def test_generate_restrictions_block():
    restrictions_config = {
        "restrictions": {"users": ["user1", "user2"], "teams": ["team1", "team2"]}
    }
    result = generate_restrictions_block(restrictions_config)
    expected_result = '  restrictions {\n  users = ["user1", "user2"]\n  teams = ["team1", "team2"]\n  }\n'
    assert result == expected_result


def test_parse_json_config():
    with open("tests/test_config.json", "w") as f:
        json.dump([{"name": "test_repo"}], f)

    result = parse_json_config("tests/test_config.json")
    assert 'resource "github_repository" "test_repo"' in result
