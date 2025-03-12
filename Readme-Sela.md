# GCP Landing Zone & Infrastructure

This infrastructure was forked from, and deployed using Google's Cloud Foundation Fabric FAST Terraform repo. The repo can be found here, with relevant documentation: https://github.com/GoogleCloudPlatform/cloud-foundation-fabric

## Features
Using the FAST methodology brings many benefits to managing the infrastructure. Resource organization best-practices are implemented via a default folder structure, containing Development and Production subfolders where relevant. New folders, projects and other configuration elements can easily be added via YAML configuration files which are interpreted by the Terraform stacks to easily create and modify resources.

Additionally, baseline organizational security policies are applied by Terraform, including best practices like disallowing public access to resources by default.  A full list of policies can be viewed here, filtering for Enforcement State: "Active": [Organization Policies](https://console.cloud.google.com/iam-admin/orgpolicies/list?organizationId=504844200547&supportedpurview=project&pageState=(%22OrgPoliciesTable%22:(%22f%22:%22%255B%257B_22k_22_3A_22Enforcement%2520state_22_2C_22t_22_3A10_2C_22v_22_3A_22_5C_22_5C_5C_5C_22Active_5C_5C_5C_22_5C_22_22_2C_22i_22_3A_22enforcementState_22%257D%255D%22)))

## Common Tasks
### Terraform changes
To deploy changes to the Terraform, you'll need to set up some prerequisites, pull down a copy of the Terraform repo, and then choose the relevant FAST stage or resource stack for deployment. Example for macOS with Homebrew installed:
```
# Deployment example

brew install --cask google-cloud-sdk
gcloud auth login
gcloud auth application-default login
cd kissplatform-gcp-lz/fast/stages/2-project-factory
terraform plan
```
### Add a folder
### Add a project
