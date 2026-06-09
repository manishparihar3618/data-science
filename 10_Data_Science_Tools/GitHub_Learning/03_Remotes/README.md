# Git Remotes

## What is a Remote?
A remote is an online Git repository (usually on GitHub) connected to your local project.
It allows you to:

- Push code to GitHub
- Pull latest changes
- Collaborate with others
- Backup your project online

## Common Commands
bash
# View remotes
git remote -v
# Add remote
git remote add origin <repo-url>
# Remove remote
git remote remove origin
# Push code
git push origin main
# Pull latest changes
git pull origin main
## Note
origin is the default name of the GitHub repository connected to your local project.