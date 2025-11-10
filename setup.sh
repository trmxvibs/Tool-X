#!/bin/bash

# setup.sh - Tool-X Centralized Installation Script
# This script handles all prerequisites, mirror fixes, and sets up the global 'toolx' alias.

TOOL_DIR="$HOME/tool-x"
REPO_URL="https://github.com/trmxvibs/Tool-X" 
INSTALLER_SCRIPT="tool-x.py"
ALIAS_NAME="toolx"

# Define colors for basic messages
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
RED='\033[1;31m'
NC='\033[0m' # No Color

echo -e "\n${GREEN}================================================${NC}"
echo -e "${GREEN}       Tool-X Setup Wizard: Initializing${NC}"
echo -e "${GREEN}================================================${NC}"

# 1. Fix Mirrors and Update Packages
echo -e "\n${YELLOW}[*] Attempting to fix Termux repositories and updating packages...${NC}"
termux-change-repo 
pkg update -y

# 2. Install Core Dependencies (Git, Python, Figlet, Ruby)
echo -e "\n${YELLOW}[*] Installing core system dependencies (git, python, figlet, ruby)...${NC}"
pkg install git python figlet ruby -y

# 3. Fix Lolcat (Using Ruby Gem Manager)
echo -e "\n${YELLOW}[*] Installing lolcat via Ruby Gem (Fix for common Termux error)...${NC}"
# SC2181 Fix: We run the command and check its status directly.
if ! gem install lolcat; then  # Fix for line 38 area
    echo -e "${RED}[!] WARNING: 'gem install lolcat' failed. Banner may not be colored. Manual check needed.${NC}"
fi

# 4. Install Python Library (colorama)
echo -e "\n${YELLOW}[*] Installing required Python library (colorama)...\033[0m"
pip install colorama

# 5. Clone or Create the Tool Directory
if [ -d "$TOOL_DIR" ]; then
    echo -e "\n${RED}[!] Directory $TOOL_DIR already exists. Pulling latest changes...${NC}"
    cd "$TOOL_DIR" || exit
    git pull
else
    echo -e "\n${GREEN}[*] Cloning Tool-X into $TOOL_DIR...${NC}"
    # SC2181 Fix: Combined git clone and status check
    if ! git clone $REPO_URL "$TOOL_DIR"; then # Fix for line 55 area
        echo -e "${RED}[!] Git clone failed. Please ensure the repository URL is correct.${NC}"
        exit 1 # Exit if cloning fails
    fi
    cd "$TOOL_DIR" || exit
fi

# 6. Set Execution Permission
chmod +x "$INSTALLER_SCRIPT" 

# 7. Create a Centralized Access Alias
echo -e "\n${YELLOW}[*] Creating permanent alias for centralized access...${NC}"
BASHRC="$PREFIX/etc/bash.bashrc"
ALIAS_LINE="alias $ALIAS_NAME='python $TOOL_DIR/$INSTALLER_SCRIPT'"

if grep -q "$ALIAS_LINE" "$BASHRC"; then
    echo -e "${YELLOW}[!] Alias '$ALIAS_NAME' already exists. Skipping.${NC}"
else
    echo -e "\n# Tool-X Framework Alias" >> "$BASHRC"
    echo "$ALIAS_LINE" >> "$BASHRC"
    echo -e "${GREEN}[+] Alias '$ALIAS_NAME' created.${NC}"
fi

# 8. Final Banner and Instructions
echo -e "\n\n${GREEN}================================================${NC}"
echo -e "${GREEN}[!] Tool-X Installation Complete!${NC}"
figlet Tool-X | lolcat -a -d 10
echo -e "${GREEN}================================================${NC}"
echo -e "${YELLOW}You can now access the tool from anywhere by typing:${NC}"
echo -e "\n  \033[1;37m$ $ALIAS_NAME\n${NC}"
echo -e "${YELLOW}NOTE: You must restart your Termux session for the 'toolx' alias to work.${NC}"
