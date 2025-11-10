#!/bin/bash
# update_date.sh
# Automatically updates README.md with today's date and badge

README="README.md"
TODAY=$(date +"%B %d, %Y")        # Example: November 10, 2025
TIMESTAMP=$(date -d "$TODAY" +"%s")  # Converts to Unix timestamp for badge

# Generate badge markdown
BADGE="![Last Updated](https://img.shields.io/date/$TIMESTAMP?label=Last%20Update&color=orange)"
LINE="**Last updated on:** $TODAY"

# Update or insert the badge line
if grep -q "!\[Last Updated\]" "$README"; then
    sed -i "s|!\[Last Updated\].*|$BADGE|g" "$README"
else
    sed -i "1i $BADGE\n" "$README"
fi

# Update or insert the "Last updated on" line
if grep -q "\*\*Last updated on:\*\*" "$README"; then
    sed -i "s|\*\*Last updated on:\*\* .*|$LINE|g" "$README"
else
    echo -e "\n$LINE" >> "$README"
fi

echo "✅ README updated with today's date: $TODAY"
