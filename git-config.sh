#!/bin/bash

# Set static Git config values
git config --local user.name "Md Mahibul Hasan"
git config --local user.email "hyde.sohag@gmail.com"

# Confirm values
echo "Git local config set:"
git config --local user.name
git config --local user.email