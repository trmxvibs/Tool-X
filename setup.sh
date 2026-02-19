#!/bin/bash
# Author: lokesh-kumar
# Update: 19/02/2026
# setup.sh - Multi-Platform Installer Termux Optimized

TOOL_DIR="$HOME/tool-x"
REPO_URL="https://github.com/trmxvibs/Tool-X"
INSTALLER_SCRIPT="tool-x.py"
ALIAS_NAME="Tool-x"

# Define colors
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
RED='\033[1;31m'
NC='\033[0m'

echo -e "\n${GREEN}[*] Initializing Tool-X Setup...${NC}"

# --- Step 1: Detect OS & Environment ---
if [ -d "$PREFIX" ] && grep -q "com.termux" "$PREFIX/etc/bash.bashrc" 2>/dev/null; then
    IS_TERMUX=true
    echo -e "${YELLOW}[*] Environment: Termux Detected.${NC}"
else
    IS_TERMUX=false
    echo -e "${YELLOW}[*] Environment: Linux/PC Detected.${NC}"
fi

# --- Step 2: Install Dependencies ---
if [ "$IS_TERMUX" = true ]; then
    # Termux Specific Fixes
    echo -e "\n${YELLOW}[*] Updating Termux Repos...${NC}"
    pkg update -y
    
    echo -e "${YELLOW}[*] Installing dependencies (git, python)...${NC}"
    pkg install git python -y
    
else
    # Linux (Kali/Ubuntu) logic
    if command -v apt >/dev/null; then
        echo -e "\n${YELLOW}[*] Updating APT repositories...${NC}"
        sudo apt update -y
        sudo apt install git python3 python3-pip -y
    else
        echo -e "${RED}[!] 'apt' not found. Assuming dependencies are installed manually on Windows/Other Linux.${NC}"
    fi
fi

# --- Step 3: Install Python Requirements ---
echo -e "\n${YELLOW}[*] Installing Python Libraries (Rich UI)...${NC}"
pip install rich requests beautifulsoup4 --break-system-packages 2>/dev/null || pip install rich requests beautifulsoup4

# --- Step 4: Clone Repository ---
if [ -d "$TOOL_DIR" ]; then
    echo -e "\n${YELLOW}[*] Updating Tool-X...${NC}"
    cd "$TOOL_DIR" || exit
    git pull
else
    echo -e "\n${GREEN}[*] Cloning Tool-X...${NC}"
    git clone "$REPO_URL" "$TOOL_DIR"
    cd "$TOOL_DIR" || exit
fi

chmod +x "$INSTALLER_SCRIPT"

# --- Step 5: Setup Alias (Termux/Linux only) ---
if [ "$IS_TERMUX" = true ]; then
    SHELL_RC="$PREFIX/etc/bash.bashrc"
else
    SHELL_RC="$HOME/.bashrc"
fi

# Only try to set alias if RC file exists (Skips Windows CMD)
if [ -f "$SHELL_RC" ]; then
    ALIAS_CMD="alias $ALIAS_NAME='python $TOOL_DIR/$INSTALLER_SCRIPT'"
    
    if grep -q "$ALIAS_NAME=" "$SHELL_RC"; then
        echo -e "${YELLOW}[!] Alias already exists.${NC}"
    else
        echo -e "\n# Tool-X Alias" >> "$SHELL_RC"
        echo "$ALIAS_CMD" >> "$SHELL_RC"
        echo -e "${GREEN}[+] Alias '$ALIAS_NAME' added to $SHELL_RC${NC}"
    fi
fi

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}   Setup Complete! Type: $ALIAS_NAME ${NC}"
echo -e "${GREEN}========================================${NC}"

if [ "$IS_TERMUX" = true ]; then
    echo -e "${YELLOW}Please restart System to apply changes.${NC}"
fi
