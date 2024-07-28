resource "github_repository" "kom-portfolio" {
  name        = "kom-portfolio"
  description = "Repo to hold all source code for website portfolio."
  visibility  = "public"
  auto_init   = "true"
  allow_merge_commit = false
  allow_rebase_merge = false
  allow_squash_merge = true
  delete_branch_on_merge = true
  archived = false
  gitignore_template = ""
}
resource "github_branch" "kom-portfolio_main" {
  repository = github_repository.kom-portfolio.name
  branch     = "main"
}
resource "github_branch_default" "kom-portfolio_default" {
  repository = github_repository.kom-portfolio.name
  branch     = github_branch.kom-portfolio_main.branch
}
resource "github_branch_protection_v3" "kom-portfolio-protection" {
  depends_on  = [github_branch_default.kom-portfolio_default]
  repository = github_repository.kom-portfolio.name
  branch       = "main"
  required_status_checks {
  strict = true
  }
  required_pull_request_reviews {
  dismiss_stale_reviews = true
  require_code_owner_reviews = true
  }
  restrictions {
  users = ["jaredkominsky"]
  }
}
