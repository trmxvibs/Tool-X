#!/bin/bash
# update_date.sh
FILE="daily_update.txt"
CURRENT_DATE=$(date +"%Y-%m-%d %H:%M:%S")
echo "Last Updated: $CURRENT_DATE" > "$FILE"
echo "Updated $FILE with current date/time: $CURRENT_DATE"
