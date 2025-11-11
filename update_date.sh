#!/bin/bash
# update_date.sh — Updates the timestamp in README.md for the date badge

# Get current timestamp (in seconds)
timestamp=$(date +%s)

# Update the badge line in README.md
sed -i "s|https://img.shields.io/date/[0-9]*?label=Last%20Update&color=orange|https://img.shields.io/date/${timestamp}?label=Last%20Update&color=orange|" README.md
