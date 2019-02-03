#!/bin/bash
# Temporarily store uncommited changes
git stash

# Verify correct branch
git checkout develop

# Build files
python build.py
cp default.css _site/default.css
cp README.md _site/README.md
# Get previous files
git fetch --all
git checkout -b master --track origin/master

# Overwrite existing files with new files
rsync -a --filter='P _site/' --filter='P .git/' --filter='P .gitignore' --filter='P .gitattributes' --delete-excluded _site/ .
# Commit
git add -A
git commit -m "Publish."

# Push
git push origin master:master

# Restoration
git checkout develop
git branch -D master
git stash pop
