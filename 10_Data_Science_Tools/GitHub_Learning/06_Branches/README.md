# Git Branches

## What is a Branch?
A branch is an independent line of development in Git.
It allows you to work on new features without affecting the main code.

## Common Commands
bash
# View branches
git branch
# Create a branch
git branch feature-login
# Switch branch
git checkout feature-login
# Create and switch
git checkout -b feature-login
# Modern way
git switch -c feature-login
# Switch back to main
git switch main
# Delete a branch
git branch -d feature-login

## Why Use Branches?
- Develop features safely
- Fix bugs independently
- Experiment without affecting main code
- Collaborate with team members
## Note
main is the default branch that contains the stable version of the project.