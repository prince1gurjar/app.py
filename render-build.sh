#!/bin/bash

# Update package list
apt-get update 

# Install Chrome
apt-get install -y google-chrome-stable

# Install ChromeDriver
apt-get install -y chromium-chromedriver

# Set Permissions
chmod +x /usr/lib/chromium-browser/chromedriver

# Show versions (for debugging)
google-chrome --version
chromedriver --version
