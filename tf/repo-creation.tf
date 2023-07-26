resource "github_repository" "repo-creation" {
  name                   = "repo-creation"
  description            = "Repo that holds all repo configs used by KominskyOrg"
  visibility             = "private"
  allow_merge_commit     = false
  allow_rebase_merge     = false
  allow_squash_merge     = true
  delete_branch_on_merge = true
  archived               = false
  gitignore_template     = "Python"
}

resource "github_branch_protection_v3" "repo-creation-protection" {
  depends_on     = [github_branch_default.repo-creation_default]
  repository     = github_repository.repo-creation.name
  branch         = "main"
  enforce_admins = false
  required_status_checks {
    strict = true
    checks = ["ci-test"]
  }
  required_pull_request_reviews {
    dismiss_stale_reviews      = true
    dismissal_users            = []
    dismissal_teams            = []
    require_code_owner_reviews = true
  }
}

resource "github_branch" "repo-creation_main" {
  repository = github_repository.repo-creation.name
  branch     = "main"
}

resource "github_branch_default" "repo-creation_default" {
  repository = github_repository.repo-creation.name
  branch     = github_branch.repo-creation_main.branch
}
