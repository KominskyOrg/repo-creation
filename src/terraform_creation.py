import os
import glob
from config_parser import parse_json_config

def generate_all_terraform_files(config_dir_path):
    """
    Generate Terraform files for all JSON config files in the given directory.
    """
    # get a list of all JSON files in the directory
    json_files = glob.glob(os.path.join(config_dir_path, "*.json"))
    print(json_files)

    # loop through the list of files
    for json_file in json_files:
        # generate the Terraform code for this config file
        terraform_code = parse_json_config(json_file)

        # derive the output filename from the JSON filename
        # (e.g., 'config1.json' becomes 'config1.tf')
        tf_filename = f"{os.path.splitext(os.path.basename(json_file))[0]}.tf"
        tf_file_path = os.path.join(os.path.dirname(config_dir_path), "tf", tf_filename)
        os.makedirs(os.path.dirname(tf_file_path), exist_ok=True)

        # write the Terraform code to a file
        with open(tf_file_path, "w") as tf_file:
            tf_file.write(terraform_code)


# call the function
generate_all_terraform_files(os.path.join(os.getcwd(), "configs"))
