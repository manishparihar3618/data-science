# Common Git & GitHub Errors and Fixes

## 1. Repository Not Found

### Error
bash
remote: Repository not found.
fatal: repository 'https://github.com/username/repository.git/' not found
### Cause
- Wrong repository URL
- Wrong username
- Repository deleted
- No access permission
### Fix
bash
git remote -v
git remote remove origin
git remote add origin https://github.com/username/repository.git
git remote -v

---

## 2. Remote Origin Already Exists
### Error
bash
error: remote origin already exists
### Cause
A remote named origin is already configured.

### Fix
bash
git remote -v

git remote remove origin

git remote add origin https://github.com/username/repository.git


---

## 3. Authentication Failed

### Error
bash
remote: Support for password authentication was removed
fatal: Authentication failed
### Cause
GitHub no longer accepts account passwords.
### Fix
bash
git remote -v
git push origin main


Use:
- Personal Access Token (PAT)
- GitHub Login in VS Cod
---

## 4. Failed To Push Some Refs

### Error
bash
failed to push some refs
### Cause
Remote repository contains newer commits.
### Fix
bash
git pull origin main

git push origin main


---

## 5. Nothing To Commit

### Error
bash
nothing to commit, working tree clean
### Cause
No new changes detected.
### Fix
bash
git status

Modify files and then:

bash
git add .

git commit -m "Updated files"

---

## 7. Branch Does Not Exist

### Error
bash
error: src refspec main does not match any
### Cause
No commits exist yet or wrong branch name.
### Fix
bash
git add .
git commit -m "Initial commit"
git branch -M main
git push -u origin main

---

# Most Used Git Commands

bash
git status
git add .
git commit -m "message"
git push origin main
git pull origin main
git remote -v
git branch
git checkout main
git switch main