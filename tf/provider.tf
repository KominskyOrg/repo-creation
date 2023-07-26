provider "github" {
  token = data.aws_ssm_parameter.github_token.value
  owner = "KominskyOrg"
}

provider "aws" {
  region = "us-east-1"
}
