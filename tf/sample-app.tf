resource "github_repository" "sample-app" {
  name        = "sample-app"
  description = "My awesome repo"
  visibility  = "private"
  homepage_url = "https://example.com"
  has_issues = true
  has_projects = true
  has_wiki = true
  allow_merge_commit = true
  allow_rebase_merge = true
  allow_squash_merge = true
  delete_branch_on_merge = false
  archived = false
  license_template = "mit"
  gitignore_template = "Python"
}
resource "github_branch_protection_v3" "sample-app-protection" {
  repository = github_repository.sample-app.node_id
  branch       = "main"
  enforce_admins = false
  required_status_checks {
    strict   = true
    checks = ["ci/test"]
  }
  required_pull_request_reviews {
    dismiss_stale_reviews = true
    dismissal_users = ["user1", "user2"]
    dismissal_teams = ["team1", "team2"]
    require_code_owner_reviews = true
  }
}
