terraform {
  required_version = ">= 1.5.0"

  backend "s3" {
    bucket         = "tf-statelock"
    key            = "repo-creation.tfstate"
    region         = "us-east-1"
    dynamodb_table = "tf-state-table"
    encrypt        = true
  }
}
