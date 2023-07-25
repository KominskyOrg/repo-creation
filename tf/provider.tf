provider "github" {
  token        = data.aws_ssm_parameter.github_token.value
  organization = "KomninskyOrg"
}

provider "aws" {
  region = "us-east-1"
}
