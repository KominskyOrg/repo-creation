resource "github_repository" "kom-python-logging" {
  name        = "kom-python-logging"
  description = "Repo to hold logging package for KominskyOrg python logging."
  visibility  = "public"
  auto_init   = "true"
  allow_merge_commit = false
  allow_rebase_merge = false
  allow_squash_merge = true
  delete_branch_on_merge = true
  archived = false
  gitignore_template = ""
}
resource "github_branch" "kom-python-logging_main" {
  repository = github_repository.kom-python-logging.name
  branch     = "main"
}
resource "github_branch_default" "kom-python-logging_default" {
  repository = github_repository.kom-python-logging.name
  branch     = github_branch.kom-python-logging_main.branch
}
resource "github_branch_protection_v3" "kom-python-logging-protection" {
  depends_on  = [github_branch_default.kom-python-logging_default]
  repository = github_repository.kom-python-logging.name
  branch       = "main"
  required_status_checks {
  strict = true
  contexts = ["test"]
  }
  required_pull_request_reviews {
  dismiss_stale_reviews = true
  require_code_owner_reviews = true
  }
  restrictions {
  users = ["jaredkominsky"]
  }
}
