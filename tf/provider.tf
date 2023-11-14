provider "github" {
  token = data.aws_ssm_parameter.github_token.value
  owner = "KominskyOrg"
}

provider "aws" {
  region     = "us-east-1"
  access_key = var.AWS_ACCESS_KEY_ID
  secret_key = var.AWS_SECRET_ACCESS_KEY
}
