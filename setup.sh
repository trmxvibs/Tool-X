#!/bin/bash
# Author: Lokesh Kumar
# Update: 08/03/2026
# setup.sh 

TOOL_DIR="$HOME/tool-x"
REPO_URL="https://github.com/trmxvibs/Tool-X"
INSTALLER_SCRIPT="tool-x.py"
ALIAS_NAME="Tool-x"

# Define colors
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
RED='\033[1;31m'
NC='\033[0m'

echo -e "\n${GREEN}[*] Initializing Tool-X Universal Setup...${NC}"

# >> Step 1: Detect Environment & Install Dependencies ---
echo -e "${YELLOW}[*] Detecting Operating System and Package Manager...${NC}"

if [ -d "$PREFIX" ] && grep -q "com.termux" "$PREFIX/etc/bash.bashrc" 2>/dev/null; then
    IS_TERMUX=true
    echo -e "${GREEN}[+] Environment: Termux Detected.${NC}"
    pkg update -y
    pkg install git python -y
else
    IS_TERMUX=false
    #>> Smart Package Manager Detection for Linux/Mac
    if command -v apt-get >/dev/null; then
        echo -e "${GREEN}[+] Environment: Debian/Ubuntu/Kali/Parrot Detected.${NC}"
        sudo apt-get update -y
        sudo apt-get install git python3 python3-pip -y
    elif command -v pacman >/dev/null; then
        echo -e "${GREEN}[+] Environment: Arch/Manjaro/BlackArch Detected.${NC}"
        sudo pacman -Sy --noconfirm git python python-pip
    elif command -v dnf >/dev/null; then
        echo -e "${GREEN}[+] Environment: Fedora/RedHat Detected.${NC}"
        sudo dnf install -y git python3 python3-pip
    elif command -v brew >/dev/null; then
        echo -e "${GREEN}[+] Environment: macOS (Homebrew) Detected.${NC}"
        brew install git python
    else
        echo -e "${YELLOW}[!] Package manager not recognized (Windows/GitBash?). Please install Git and Python manually.${NC}"
    fi
fi

# >>> Step 2: Install Python Requirements ---
echo -e "\n${YELLOW}[*] Installing Python Libraries (Rich UI)...${NC}"
# >>break-system-packages is used for newer Python versions (PEP 668)
pip install rich requests beautifulsoup4 --break-system-packages 2>/dev/null || pip install rich requests beautifulsoup4

# >> Step 3: Clone or Update Repository ---
if [ -d "$TOOL_DIR" ]; then
    echo -e "\n${YELLOW}[*] Updating Tool-X...${NC}"
    cd "$TOOL_DIR" || exit
    git pull
else
    echo -e "\n${GREEN}[*] Cloning Tool-X...${NC}"
    git clone "$REPO_URL" "$TOOL_DIR"
    cd "$TOOL_DIR" || exit
fi

chmod +x "$INSTALLER_SCRIPT" 2>/dev/null || true

# >> Step 4: Smart Alias Setup (Handles bash and zsh) ---
echo -e "\n${YELLOW}[*] Setting up shortcut command...${NC}"

if [ "$IS_TERMUX" = true ]; then
    SHELL_RC="$PREFIX/etc/bash.bashrc"
else
    # Check if user is using zsh (Default in Kali & Mac)
    if [ "$(basename "$SHELL")" = "zsh" ]; then
        SHELL_RC="$HOME/.zshrc"
    else
        SHELL_RC="$HOME/.bashrc"
    fi
fi

if [ -f "$SHELL_RC" ]; then
    ALIAS_CMD="alias $ALIAS_NAME='python $TOOL_DIR/$INSTALLER_SCRIPT'"
    
    if grep -q "alias $ALIAS_NAME=" "$SHELL_RC"; then
        echo -e "${YELLOW}[!] Alias '$ALIAS_NAME' already exists in $SHELL_RC.${NC}"
    else
        echo -e "\n# Tool-X Alias" >> "$SHELL_RC"
        echo "$ALIAS_CMD" >> "$SHELL_RC"
        echo -e "${GREEN}[+] Shortcut '$ALIAS_NAME' added to $SHELL_RC${NC}"
    fi
else
    echo -e "${YELLOW}[!] Shell config file not found. Run tool manually: python $TOOL_DIR/$INSTALLER_SCRIPT${NC}"
fi

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}   Setup Complete! Type: $ALIAS_NAME ${NC}"
echo -e "${GREEN}========================================${NC}"

if [ "$IS_TERMUX" = true ]; then
    echo -e "${YELLOW}Please restart Termux to apply changes.${NC}"
else
    echo -e "${YELLOW}Please restart your terminal or type: source $SHELL_RC${NC}"
fi
