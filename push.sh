#!/bin/bash
# Temporarily store uncommited changes
git stash

# Verify correct branch
git checkout develop

# Build files
python build.py > _site/index.html
cp default.css _site/default.css
cp problems.yaml _site/problems.yaml

# Get previous files
git fetch --all
git checkout -b master --track origin/master

# Overwrite existing files with new files
mv _site/index.html index.html
mv _site/default.css default.css
mv _site/problems.yaml problems.yaml

# Commit
git add -A
git commit -m "Publish."

# Push
git push origin master:master

# Restoration
git checkout develop
git branch -D master
git stash pop
