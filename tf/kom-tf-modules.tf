resource "github_repository" "kom-tf-modules" {
  name        = "kom-tf-modules"
  description = "Repo that holds all modules used by KominskyOrg"
  visibility  = "private"
  allow_merge_commit = false
  allow_rebase_merge = false
  allow_squash_merge = true
  delete_branch_on_merge = true
  archived = false
  gitignore_template = "Terraform"
}
resource "github_branch" "kom-tf-modules_main" {
  repository = github_repository.kom-tf-modules.name
  branch     = "main"
}
resource "github_branch_default" "kom-tf-modules_default" {
  repository = github_repository.kom-tf-modules.name
  branch     = github_branch.kom-tf-modules_main.branch
}
resource "github_branch_protection_v3" "kom-tf-modules-protection" {
  depends_on  = [github_branch_default.kom-tf-modules_default]
  repository = github_repository.kom-tf-modules.name
  branch       = "main"
}
