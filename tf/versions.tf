terraform {
  required_version = ">= 1.6.0"

  cloud {
    hostname     = "app.terraform.io"
    organization = "KominskyOrg"
    workspaces {
      tags = ["repo-creation"]
    }
  }
}
