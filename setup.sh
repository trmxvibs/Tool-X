#!/bin/bash
# Author: Lokesh Kumar
# Update: 28/03/2026
# Project: Tool-X Universal Installer

TOOL_DIR="$HOME/tool-x"
REPO_URL="https://github.com/trmxvibs/Tool-X"
INSTALLER_SCRIPT="tool-x.py"

# User-friendly command variations (Case-insensitivity)
COMMANDS=("toolx" "Toolx" "Tool-x" "tool-x")

# Colors for UI
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
RED='\033[1;31m'
NC='\033[0m'

echo -e "\n${GREEN}[*] Initializing Tool-X Universal Setup...${NC}"

# --- STEP 1: Advanced OS & Package Manager Detection ---
echo -e "${YELLOW}[*] Detecting Operating System and Package Manager...${NC}"

if [ -d "$PREFIX" ] && grep -q "com.termux" "$PREFIX/etc/bash.bashrc" 2>/dev/null; then
    # 1. Termux (Android)
    OS_TYPE="termux"
    BIN_DIR="$PREFIX/bin"
    echo -e "${GREEN}[+] Environment: Termux Detected.${NC}"
    pkg update -y && pkg install git python -y

elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    # 2. Windows (Git Bash / MSYS2)
    OS_TYPE="windows"
    echo -e "${GREEN}[+] Environment: Windows Detected.${NC}"
    # Windows users need to have Git and Python installed manually

elif [[ "$OSTYPE" == "darwin"* ]]; then
    # 3. macOS
    OS_TYPE="macos"
    BIN_DIR="/usr/local/bin"
    echo -e "${GREEN}[+] Environment: macOS (Homebrew) Detected.${NC}"
    if command -v brew >/dev/null; then
        brew install git python
    else
        echo -e "${RED}[!] Homebrew not found. Please install Homebrew first.${NC}"
    fi

else
    # 4. Linux Distributions (Debian, Ubuntu, Kali, Parrot, Arch, Manjaro, BlackArch, Fedora, RedHat)
    OS_TYPE="linux"
    BIN_DIR="/usr/local/bin"
    
    if command -v apt-get >/dev/null; then
        echo -e "${GREEN}[+] Environment: Debian/Ubuntu/Kali/Parrot Detected.${NC}"
        sudo apt-get update -y && sudo apt-get install git python3 python3-pip -y
    elif command -v pacman >/dev/null; then
        echo -e "${GREEN}[+] Environment: Arch/Manjaro/BlackArch Detected.${NC}"
        sudo pacman -Sy --noconfirm git python python-pip
    elif command -v dnf >/dev/null; then
        echo -e "${GREEN}[+] Environment: Fedora/RedHat Detected.${NC}"
        sudo dnf install -y git python3 python3-pip
    else
        echo -e "${RED}[!] Unknown Linux Distro. Attempting manual dependency check...${NC}"
    fi
fi

# --- STEP 2: Python Libraries Setup ---
echo -e "\n${YELLOW}[*] Installing Python Libraries (Rich UI)...${NC}"
# Handling PEP 668 for newer Linux distros
pip install rich requests beautifulsoup4 --break-system-packages 2>/dev/null || pip install rich requests beautifulsoup4

# --- STEP 3: Clone or Update Tool-X ---
if [ -d "$TOOL_DIR" ]; then
    echo -e "\n${YELLOW}[*] Updating Tool-X Repository...${NC}"
    cd "$TOOL_DIR" || exit
    git pull
else
    echo -e "\n${GREEN}[*] Cloning Tool-X Repository...${NC}"
    git clone "$REPO_URL" "$TOOL_DIR"
    cd "$TOOL_DIR" || exit
fi
chmod +x "$INSTALLER_SCRIPT" 2>/dev/null || true

# --- STEP 4: Centralization (The Global Shortcut Logic) ---
echo -e "\n${YELLOW}[*] Centralizing Commands for Global Access...${NC}"

if [ "$OS_TYPE" == "windows" ]; then
    # Windows CMD/PowerShell Support (.bat files)
    for cmd in "${COMMANDS[@]}"; do
        echo "@echo off" > "$TOOL_DIR/$cmd.bat"
        echo "python \"$TOOL_DIR/$INSTALLER_SCRIPT\" %*" >> "$TOOL_DIR/$cmd.bat"
    done
    # Git Bash Support (Linux-like wrapper in ~/bin)
    mkdir -p "$HOME/bin"
    for cmd in "${COMMANDS[@]}"; do
        echo "python \"$TOOL_DIR/$INSTALLER_SCRIPT\" \"\$@\"" > "$HOME/bin/$cmd"
        chmod +x "$HOME/bin/$cmd"
    done
    echo -e "${GREEN}[+] Windows Batch and Bash wrappers created.${NC}"

else
    # Linux, macOS, and Termux (Global binary creation)
    SUDO_CMD=""
    [ "$OS_TYPE" != "termux" ] && SUDO_CMD="sudo"

    for cmd in "${COMMANDS[@]}"; do
        WRAPPER="#!/bin/bash\npython3 \"$TOOL_DIR/$INSTALLER_SCRIPT\" \"\$@\""
        if [ "$OS_TYPE" == "termux" ]; then
             echo -e "$WRAPPER" > "$BIN_DIR/$cmd"
             chmod +x "$BIN_DIR/$cmd"
        else
             echo -e "$WRAPPER" | $SUDO_CMD tee "$BIN_DIR/$cmd" > /dev/null
             $SUDO_CMD chmod +x "$BIN_DIR/$cmd"
        fi
    done
    echo -e "${GREEN}[+] Centralized commands created in $BIN_DIR${NC}"
fi

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}   Setup Complete! Type: toolx ${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "${YELLOW}Supported Commands: ${NC}${COMMANDS[*]}"

if [ "$OS_TYPE" == "windows" ]; then
    echo -e "\n${RED}[!] Windows Note:${NC} Add '$TOOL_DIR' to your System PATH to use commands in CMD."
fi
