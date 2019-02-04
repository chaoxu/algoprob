#!/bin/bash
# Temporarily store uncommited changes
git stash

# Verify correct branch
git checkout develop

# Build files
python build.py production
cp default.css _site/default.css
cp README.md _site/README.md
cp .gitignore _site/.gitignore
cp CNAME _site/CNAME
# Get previous files
git fetch --all
git checkout -b master --track origin/master

# Overwrite existing files with new files
rsync -a --filter='P _site/' --filter='P .git/' --filter='P .gitattributes' --delete-excluded _site/ .
# Commit
git add -A
git commit -m "Publish."

# Push
git push origin master:master

# Restoration
git checkout develop
git branch -D master
git stash pop
