import os
import sys
from time import sleep
from modules.logo import *
from modules.system import *

# Colors for terminal output
yellow = "\033[1;33m"
blue = "\033[1;34m"
nc = "\033[00m"  # No color

class Tool:
    @classmethod
    def install(cls):
        while True:
            system = sys()  # Get system configuration
            os.system("clear")
            logo.ins_tnc()  # Display terms and conditions

            inp = input(f"{yellow}Do you want to install Tool-X [Y/n]> {nc}")
            if inp.lower() == "y":
                os.system("clear")
                logo.installing()  # Display installation progress

                # Determine if sudo is available
                sudo_prefix = system.sudo if system.sudo else ""
                conf_dir = os.path.join(system.conf_dir, "Tool-X")
                toolx_path = os.path.join(system.bin, "Tool-X")
                toolx_alt_path = os.path.join(system.bin, "toolx")

                # Create configuration directory if it doesn't exist
                if not os.path.exists(conf_dir):
                    os.system(f"{sudo_prefix} mkdir -p {conf_dir}")

                # Copy necessary files to configuration and binary directories
                os.system(f"{sudo_prefix} cp -r modules core Tool-X.py {conf_dir}")
                os.system(f"{sudo_prefix} cp -r core/Tool-X {system.bin}")
                os.system(f"{sudo_prefix} cp -r core/toolx {system.bin}")

                # Set execute permissions
                os.system(f"{sudo_prefix} chmod +x {toolx_path}")
                os.system(f"{sudo_prefix} chmod +x {toolx_alt_path}")

                # Clean up installation folder
                os.system(f"cd .. && {sudo_prefix} rm -rf Tool-X")

                # Verify installation
                if os.path.exists(toolx_path) and os.path.exists(conf_dir):
                    os.system("clear")
                    logo.ins_sc()  # Show successful installation message
                    input(f"{blue}Tool-X{nc}@{blue}space {yellow}$ {nc}")
                    break
                else:
                    os.system("clear")
                    logo.not_ins()  # Show failed installation message
                    input(f"{blue}Tool-X{nc}@{blue}space {yellow}$ {nc}")
                    break
            else:
                break

if __name__ == "__main__":
    try:
        Tool.install()
    except KeyboardInterrupt:
        os.system("clear")
        logo.exit()  # Display exit message
