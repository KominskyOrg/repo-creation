resource "github_repository" "your-repo-name" {
  name        = "your-repo-name"
  description = ""
  visibility  = "private"
  homepage_url = ""
  has_issues = false
  has_projects = false
  has_wiki = false
  is_template = false
  allow_merge_commit = false
  allow_rebase_merge = false
  allow_squash_merge = false
  delete_branch_on_merge = false
  archived = false
  topics = []
  vulnerability_alerts = false
  license_template = ""
  gitignore_template = ""
}
resource "github_branch" "your-repo-name_main" {
  repository = github_repository.your-repo-name.name
  branch     = "main"
}
resource "github_branch_default" "your-repo-name_default" {
  repository = github_repository.your-repo-name.name
  branch     = github_branch.your-repo-name_main.branch
}
resource "github_branch_protection_v3" "your-repo-name-protection" {
  depends_on  = [github_branch_default.your-repo-name_default]
  repository = github_repository.your-repo-name.name
  branch       = "main"
  enforce_admins = false
  required_status_checks {
  strict = false
  }
  required_pull_request_reviews {
  dismiss_stale_reviews = false
  dismissal_users = []
  dismissal_teams = []
  require_code_owner_reviews = false
  }
  restrictions {
  users = []
  teams = []
  }
}
