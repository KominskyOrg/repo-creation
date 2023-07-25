data "aws_ssm_parameter" "github_token" {
    name = var.github_token_ssm_name
}