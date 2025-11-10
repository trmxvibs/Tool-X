#!/bin/bash

# setup.sh - Tool-X Centralized Installation Script
# Handles prerequisites, mirror fixes, and sets up a global alias.

TOOL_DIR="$HOME/tool-x"
REPO_URL="https://github.com/trmxvibs/Tool-X"
INSTALLER_SCRIPT="tool-x.py"
ALIAS_NAME="toolx"

# Define colors
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
RED='\033[1;31m'
NC='\033[0m' # No Color

echo -e "\n${GREEN}================================================${NC}"
echo -e "${GREEN}       Tool-X Setup Wizard: Initializing${NC}"
echo -e "${GREEN}================================================${NC}"

# 1. Fix mirrors and update packages
echo -e "\n${YELLOW}[*] Fixing Termux repositories and updating packages...${NC}"
termux-change-repo
pkg update -y

# 2. Install core dependencies
echo -e "\n${YELLOW}[*] Installing core dependencies (git, python, figlet, ruby)...${NC}"
pkg install git python figlet ruby -y

# 3. Install lolcat using Ruby gem
echo -e "\n${YELLOW}[*] Installing lolcat via Ruby Gem (fix for Termux error)...${NC}"
if ! gem install lolcat; then
    echo -e "${RED}[!] WARNING: 'gem install lolcat' failed. Banner may not be colored.${NC}"
fi

# 4. Install required Python library
echo -e "\n${YELLOW}[*] Installing Python library (colorama)...${NC}"
pip install colorama

# 5. Clone or update the Tool-X repository
if [ -d "$TOOL_DIR" ]; then
    echo -e "\n${RED}[!] Directory $TOOL_DIR exists. Pulling latest changes...${NC}"
    cd "$TOOL_DIR" || exit
    git pull
else
    echo -e "\n${GREEN}[*] Cloning Tool-X into $TOOL_DIR...${NC}"
    if ! git clone "$REPO_URL" "$TOOL_DIR"; then
        echo -e "${RED}[!] Git clone failed. Please check your internet connection or repo URL.${NC}"
        exit 1
    fi
    cd "$TOOL_DIR" || exit
fi

# 6. Make main script executable
chmod +x "$INSTALLER_SCRIPT"

# 7. Create a centralized alias
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

# 8. Display final banner
echo -e "\n\n${GREEN}================================================${NC}"
echo -e "${GREEN}[!] Tool-X Installation Complete!${NC}"
figlet Tool-X | lolcat -a -d 10
echo -e "${GREEN}================================================${NC}"
echo -e "${YELLOW}You can now access the tool by typing:${NC}"
echo -e "\n  \033[1;37m$ $ALIAS_NAME\n${NC}"
echo -e "${YELLOW}NOTE: Restart Termux for the 'toolx' alias to work.${NC}"
