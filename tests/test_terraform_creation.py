from unittest.mock import patch, mock_open
from src.terraform_creation import generate_all_terraform_files


def mock_os_path_join(*args):
    if args == ("/path/to", "*.json"):
        return "/path/to/config1.json"
    elif args[0].startswith("/path/to") and args[1] == "config1.json":
        return "/path/to/config1.json"
    else:
        return "/path/to/tf/config1.tf"


def test_generate_all_terraform_files():
    with patch("glob.glob", return_value=["/path/to/config1.json"]), patch(
        "os.path.join", side_effect=mock_os_path_join
    ), patch("os.getcwd", return_value="/path/to"), patch(
        "os.path.splitext", return_value=("/path/to/config1", ".json")
    ), patch(
        "os.path.basename", return_value="config1.json"
    ), patch(
        "os.path.dirname", return_value="/path/to"
    ), patch(
        "os.makedirs", return_value=None
    ), patch(
        "builtins.open", mock_open()
    ) as m, patch(
        "src.terraform_creation.parse_json_config", return_value="terraform_code"
    ):
        generate_all_terraform_files("/path/to")

        # Assert the file was written to as expected
        m.assert_called_once_with("/path/to/tf/config1.tf", "w")


def test_generate_all_terraform_files_no_json_files():
    with patch("glob.glob", return_value=[]), patch(
        "os.path.join", return_value="/path/to/configs"
    ), patch("os.getcwd", return_value="/path/to"), patch(
        "os.path.splitext", return_value=("/path/to/config1", ".json")
    ), patch(
        "os.path.basename", return_value="config1.json"
    ), patch(
        "os.path.dirname", return_value="/path/to"
    ), patch(
        "os.makedirs", return_value=None
    ), patch(
        "builtins.open", mock_open()
    ) as m, patch(
        "src.terraform_creation.parse_json_config", return_value="terraform_code"
    ):
        generate_all_terraform_files("/path/to")

        # Assert that the file write did not occur
        m.assert_not_called()
