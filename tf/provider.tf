provider "github" {
  token = data.aws_ssm_parameter.github_token.value
  owner = "KomninskyOrg"
}

provider "aws" {
  region = "us-east-1"
}
