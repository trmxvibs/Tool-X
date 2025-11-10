# File: core/tool_data.py
# Date 08/11/2025
# Github : https://github.com/trmxvibs
# Author : Lokesh kumar
# File: core/tool_data.py

# This file contains the structured data for all tools to be included in the Tool-X Installer.

TOOL_CATEGORIES = {
    "01": "OSINT & Information Retrieval",
    "02": "Social Engineering & Phishing",
    "03": "Bruteforce & Password Attacks",
    "04": "Stress Testing & Spamming Tools",
    "05": "Linux & Desktop Installation",
    "06": "Termux Utilities & Add-ons",
    "07": "All-in-One Hacking Frameworks"
}

# Define the tools for each category.
# Format: "tool_number": { "name": "Tool Name", "desc": "Short description", "repo": "GitHub URL", "reqs": "Required Termux packages", "install_cmd": "Custom install command", "help_cmd": "Command to display help/run" }

TOOLS = {
    "01": { # OSINT & Information Retrieval
        "01": {"name": "GhostTrack", "desc": "Track location or mobile number", "repo": "https://github.com/HunxByts/GhostTrack", "reqs": "python", "install_cmd": "pip install -r requirements.txt", "help_cmd": "python GhostTrack.py -h"},
        "02": {"name": "snoop", "desc": "Open-source intelligence (OSINT) scanner", "repo": "https://github.com/snooppr/snoop", "reqs": "python", "install_cmd": "pip install -r requirements.txt", "help_cmd": "python snoop.py -h"},
        "03": {"name": "IP-Tracer", "desc": "Retrieve any IP address information", "repo": "https://github.com/rajkumardusad/IP-Tracer", "reqs": "php", "install_cmd": "./install", "help_cmd": "bash ip-tracer.sh -t"},
        "04": {"name": "PhoneInfoga", "desc": "Scan phone numbers using free resources", "repo": "https://github.com/ExpertAnonymous/PhoneInfoga", "reqs": "python", "help_cmd": "python phoneinfoga.py -h"},
        "05": {"name": "X-osint", "desc": "OSINT framework for phone number/email", "repo": "https://github.com/TermuxHackz/X-osint", "reqs": "python", "help_cmd": "python x-osint.py -h"},
        "06": {"name": "Mr.Holmes", "desc": "A complete OSINT Tool", "repo": "https://github.com/Lucksi/Mr.Holmes", "reqs": "python", "help_cmd": "python mrholmes.py -h"},
        "07": {"name": "UserFinder", "desc": "OSINT tool for finding profiles by username", "repo": "https://github.com/mishakorzik/UserFinder", "reqs": "bash", "help_cmd": "./userfinder.sh"},
        "08": {"name": "osi.ig", "desc": "Information Gathering for Instagram", "repo": "https://github.com/th3unkn0n/osi.ig", "reqs": "python", "install_cmd": "pip install -r requirements.txt", "help_cmd": "python osi.ig.py -h"},
        "09": {"name": "ipdrone", "desc": "Track location with live address and accuracy", "repo": "https://github.com/noob-hackers/ipdrone", "reqs": "python", "help_cmd": "python ipdrone.py -h"},
        "10": {"name": "SIGIT", "desc": "Simple Information Gathering Toolkit", "repo": "https://github.com/termuxhackers-id/SIGIT", "reqs": "python", "help_cmd": "python sigit.py"},
        "11": {"name": "infoooze", "desc": "OSINT tool to quickly find information effectively", "repo": "https://github.com/devxprite/infoooze", "reqs": "nodejs", "install_cmd": "npm install", "help_cmd": "node infoooze.js -h"},
        "12": {"name": "IpHack", "desc": "Track location with live address and city", "repo": "https://github.com/mishakorzik/IpHack", "reqs": "bash", "help_cmd": "bash iphack.sh"}
    },
    "02": { # Social Engineering & Phishing
        "01": {"name": "nexphisher", "desc": "Advanced Phishing tool", "repo": "https://github.com/htr-tech/nexphisher", "reqs": "bash php", "help_cmd": "bash nexphisher.sh"},
        "02": {"name": "CamPhish", "desc": "Grab cam shots & GPS location via link", "repo": "https://github.com/techchipnet/CamPhish", "reqs": "php", "help_cmd": "bash camphish.sh"},
        "03": {"name": "maskphish", "desc": "URL making technology (Phishing URL Mask)", "repo": "https://github.com/jaykali/maskphish", "reqs": "bash", "help_cmd": "bash maskphish.sh -h"},
        "04": {"name": "mrphish", "desc": "All-in-one social phishing (with Otp Bypass)", "repo": "https://github.com/noob-hackers/mrphish", "reqs": "bash", "help_cmd": "bash mrphish.sh"},
        "05": {"name": "ShellPhish", "desc": "Modded version of shellphish", "repo": "https://github.com/AbirHasan2005/ShellPhish", "reqs": "bash", "help_cmd": "bash shellphish.sh"},
        "06": {"name": "symbiote", "desc": "Access phone cameras via link (phishing)", "repo": "https://github.com/hasanfirnas/symbiote", "reqs": "python", "help_cmd": "python symbiote.py -h"},
        "07": {"name": "grabcam/seeu", "desc": "Tool to hack camera from termux", "repo": "https://github.com/noob-hackers/grabcam", "reqs": "bash", "help_cmd": "bash grabcam.sh"},
        "08": {"name": "infect", "desc": "Infect any Android device with Virus From Link", "repo": "https://github.com/noob-hackers/infect", "reqs": "bash", "help_cmd": "bash infect.sh"},
        "09": {"name": "hacklock", "desc": "Hack Android Pattern from Termux", "repo": "https://github.com/noob-hackers/hacklock", "reqs": "bash", "help_cmd": "bash hacklock.sh"},
        "10": {"name": "FluxER", "desc": "Installs and runs Fluxion inside Termux (Wi-Fi attack)", "repo": "https://github.com/0n1cOn3/FluxER", "reqs": "bash", "help_cmd": "bash fluxer.sh"},
        "11": {"name": "hackerpro", "desc": "All in One Hacking Tool for Android", "repo": "https://github.com/jaykali/hackerpro", "reqs": "python", "help_cmd": "python hackerpro.py"}
    },
    "03": { # Bruteforce & Password Attacks
        "01": {"name": "SocialBox", "desc": "Bruteforce Framework (FB, Gmail, IG, Twitter)", "repo": "https://github.com/samsesh/SocialBox-Termux", "reqs": "python bash", "help_cmd": "python socialbox.py"},
        "02": {"name": "BruteFb/Facebash", "desc": "Facebook Bruteforce via Tor", "repo": "https://github.com/th3unkn0n/facebash-termux", "reqs": "bash", "help_cmd": "bash facebash.sh"},
        "03": {"name": "InstaHack", "desc": "Instagram password strength test/bruteforce", "repo": "https://github.com/evildevill/instahack", "reqs": "bash", "help_cmd": "bash instahack.sh"},
        "04": {"name": "InstaBruteForce", "desc": "Bruteforce password cracker (Instagram)", "repo": "https://github.com/GH05T-HUNTER5/GH05T-INSTA", "reqs": "bash", "help_cmd": "bash gh05t-insta.sh"},
        "05": {"name": "Brutegram", "desc": "Instagram multi-bruteforce Platfrom", "repo": "https://github.com/Err0r-ICA/Brutegram", "reqs": "python", "help_cmd": "python brutegram.py"},
        "06": {"name": "GbyFB", "desc": "Facebook Hacking Tool", "repo": "https://github.com/Mr-G0b3y/GbyFB", "reqs": "python", "help_cmd": "python gbyfb.py"},
        "07": {"name": "lazybee", "desc": "Create best wordlist from Python Tool", "repo": "https://github.com/noob-hackers/lazybee", "reqs": "python", "help_cmd": "python lazybee.py"},
        "08": {"name": "Gmail-Hack", "desc": "Easy Gmail hacking in python (Bruteforce)", "repo": "https://github.com/Zard2007/Gmail-Hack", "reqs": "python", "help_cmd": "python gmail-hack.py"},
        "09": {"name": "fikrado.py", "desc": "Facebook hacking Tools script super fast", "repo": "https://github.com/fikrado/fikrado.py", "reqs": "python", "help_cmd": "python fikrado.py"},
        "10": {"name": "hackerxphantom/Facebook_hack", "desc": "Most Powerful Facebook Bruteforce Tool", "repo": "https://github.com/hackerxphantom/Facebook_hack", "reqs": "python", "help_cmd": "python facebook_hack.py"}
    },
    "04": { # Stress Testing & Spamming Tools
        "01": {"name": "TBomb", "desc": "SMS And Call Bomber", "repo": "https://github.com/TheSpeedX/TBomb", "reqs": "python", "install_cmd": "pip install -r requirements.txt", "help_cmd": "bash TBomb.sh"},
        "02": {"name": "Impulse", "desc": "Denial-of-service ToolKit (DDoS)", "repo": "https://github.com/LimerBoy/Impulse", "reqs": "python", "install_cmd": "pip install -r requirements.txt", "help_cmd": "python impulse.py -h"},
        "03": {"name": "Bombers", "desc": "SMS/Email/Whatsapp/Twitter/Instagram bombers Collection", "repo": "https://github.com/bhattsameer/Bombers", "reqs": "python", "help_cmd": "python bombers.py"},
        "04": {"name": "Beast_Bomber", "desc": "Open source bomber (DDoS/Email/SMS)", "repo": "https://github.com/un1cum/Beast_Bomber", "reqs": "python", "help_cmd": "python beast_bomber.py -h"},
        "05": {"name": "Vaim-sms", "desc": "DDoS attack on phone number", "repo": "https://github.com/VaimpierOfficial/Vaim-sms", "reqs": "python", "help_cmd": "python vaim.py"},
        "06": {"name": "WA_CRASHER", "desc": "WhatsApp Crash With one Message", "repo": "https://github.com/hackerxphantom/WA_CRASHER", "reqs": "python", "help_cmd": "python wa_crasher.py"},
        "07": {"name": "Anon-SMS", "desc": "Tool To Send Messages Anonymously", "repo": "https://github.com/HACK3RY2J/Anon-SMS", "reqs": "bash", "help_cmd": "bash anon-sms.sh"},
        "08": {"name": "spamx", "desc": "All In 1 Spam Tool For Termux Users", "repo": "https://github.com/noob-hackers/spamx", "reqs": "php", "help_cmd": "bash spamx.sh"},
        "09": {"name": "XLR8_BOMBER", "desc": "Superfast SMS & Call bomber", "repo": "https://github.com/anubhavanonymous/XLR8_BOMBER", "reqs": "python", "install_cmd": "pip install -r requirements.txt", "help_cmd": "python xlr8.py"},
        "10": {"name": "Raven-Storm", "desc": "Powerful DDoS toolkit for penetration tests", "repo": "https://github.com/Tmpertor/Raven-Storm", "reqs": "python", "help_cmd": "python raven-storm.py"}
    },
    "05": { # Linux & Desktop Installation
        "01": {"name": "Nethunter-In-Termux", "desc": "Install Kali Nethunter in Termux without root", "repo": "https://github.com/Hax4us/Nethunter-In-Termux", "reqs": "bash", "help_cmd": "./start-nethunter.sh"},
        "02": {"name": "proot-distro", "desc": "Utility for managing Linux distributions in Termux", "repo": "https://github.com/termux/proot-distro", "reqs": "bash", "help_cmd": "proot-distro list"},
        "03": {"name": "Termux-Kali/Kalimux", "desc": "Install Kali Linux on Android using Termux", "repo": "https://github.com/MasterDevX/Termux-Kali", "reqs": "bash", "help_cmd": "./install.sh"},
        "04": {"name": "TermuxArch", "desc": "Install Arch Linux in Termux", "repo": "https://github.com/TermuxArch/TermuxArch", "reqs": "bash", "help_cmd": "./setupTermuxArch.sh help"},
        "05": {"name": "TermuxAlpine", "desc": "Install Alpine Linux in Termux", "repo": "https://github.com/Hax4us/TermuxAlpine", "reqs": "bash", "help_cmd": "bash TermuxAlpine.sh"},
        "06": {"name": "ubuntu-in-termux", "desc": "Install Ubuntu in Termux without a rooted device", "repo": "https://github.com/MFDGaming/ubuntu-in-termux", "reqs": "bash", "help_cmd": "./ubuntu.sh"},
        "07": {"name": "termux-desktop", "desc": "Setup a beautiful Desktop/GUI in Termux (adi1090x)", "repo": "https://github.com/adi1090x/termux-desktop", "reqs": "bash", "help_cmd": "bash setup.sh"},
        "08": {"name": "Termux_XFCE", "desc": "Set up XFCE desktop in Termux X11", "repo": "https://github.com/phoenixbyrd/Termux_XFCE", "reqs": "bash", "help_cmd": "bash setup.sh"},
        "09": {"name": "AnLinux-App", "desc": "Run Linux on Android without root access", "repo": "https://github.com/EXALAB/AnLinux-App", "reqs": "bash", "help_cmd": "bash setup.sh"},
        "10": {"name": "modded-ubuntu", "desc": "Run Ubuntu GUI on your termux with features", "repo": "https://github.com/modded-ubuntu/modded-ubuntu", "reqs": "bash", "help_cmd": "bash install.sh"},
        "11": {"name": "ubuntu-on-android", "desc": "Run Ubuntu with pre-installed Desktop Environments", "repo": "https://github.com/RandomCoderOrg/ubuntu-on-android", "reqs": "bash", "help_cmd": "bash installer.sh"}
    },
    "06": { # Termux Utilities & Add-ons
        "01": {"name": "termux-api", "desc": "Exposes device functionality as API to command line", "repo": "termux-api", "reqs": "", "help_cmd": "termux-battery-status -h"},
        "02": {"name": "termux-x11", "desc": "Termux X-server add-on (GUI)", "repo": "termux-x11", "reqs": "", "help_cmd": "apt show termux-x11"},
        "03": {"name": "termux-styling", "desc": "Customize terminal font and color theme", "repo": "termux-styling", "reqs": "", "help_cmd": "apt show termux-styling"},
        "04": {"name": "termux-widget", "desc": "Adds shortcuts to commands on the home screen", "repo": "termux-widget", "reqs": "", "help_cmd": "apt show termux-widget"},
        "05": {"name": "Termux-ADB", "desc": "Install ADB & FastBoot Tools in Termux", "repo": "https://github.com/MasterDevX/Termux-ADB", "reqs": "bash", "help_cmd": "bash install-adb.sh"},
        "06": {"name": "T-Header", "desc": "Personalize Termux startup with custom logos/themes", "repo": "https://github.com/remo7777/T-Header", "reqs": "bash", "help_cmd": "bash t-header.sh"},
        "07": {"name": "sttr", "desc": "Cross-platform CLI app for string operations", "repo": "https://github.com/abhimanyu003/sttr", "reqs": "go", "help_cmd": "./sttr -h"},
        "08": {"name": "Revancify", "desc": "Tool for using Revanced/Revanced-Extended", "repo": "https://github.com/decipher3114/Revancify", "reqs": "bash", "help_cmd": "bash revancify.sh"},
        "09": {"name": "root-termux", "desc": "Install pseudo-root (sudo) in Termux", "repo": "https://github.com/hctilg/root-termux", "reqs": "bash", "help_cmd": "bash root-termux.sh"},
        "10": {"name": "MyServer", "desc": "Setup PHP, Apache, Nginx and MySQL servers", "repo": "https://github.com/rajkumardusad/MyServer", "reqs": "python", "help_cmd": "python myserver.py -h"},
        "11": {"name": "termux-gui", "desc": "Plugin to use native Android GUI components from CLI", "repo": "termux-gui", "reqs": "", "help_cmd": "apt show termux-gui"},
        "12": {"name": "tsu", "desc": "Gain root shell on Termux (if device is rooted)", "repo": "tsu", "reqs": "", "help_cmd": "tsu -h"},
        "13": {"name": "TermuxBlack", "desc": "Termux repository for hacking tools and packages", "repo": "https://github.com/Hax4us/TermuxBlack", "reqs": "bash", "help_cmd": "apt show termuxblack"},
        "14": {"name": "Termux-Archlinux (SDRausty)", "desc": "Install Arch Linux in Termux (SDRausty script)", "repo": "https://github.com/SDRausty/termux-archlinux", "reqs": "bash", "help_cmd": "bash setupTermuxArch.sh"},
        "15": {"name": "GURU-Ai", "desc": "Simple yet Complicated AI/Automation tool", "repo": "https://github.com/Guru322/GURU-Ai", "reqs": "nodejs", "help_cmd": "node guru.js"},
    },
    "07": { # All-in-One Hacking Frameworks
        "01": {"name": "AllHackingTools", "desc": "All-in-One Hacking Tools For Hackers", "repo": "https://github.com/mishakorzik/AllHackingTools", "reqs": "bash", "help_cmd": "bash all-hacking-tools.sh"},
        "02": {"name": "awesome-termux-hacking", "desc": "An awesome list of the best Termux hacking tools", "repo": "https://github.com/may215/awesome-termux-hacking", "reqs": "bash", "help_cmd": "cat README.md"},
        "03": {"name": "Lazymux", "desc": "Termux tool installer (similar to this framework)", "repo": "https://github.com/Gameye98/Lazymux", "reqs": "python", "help_cmd": "python lazymux.py"},
        "04": {"name": "EasY_HaCk", "desc": "Hack the World using Termux", "repo": "https://github.com/sabri-zaki/EasY_HaCk", "reqs": "python", "help_cmd": "python easy_hack.py"},
        "05": {"name": "cracker911181-Tool", "desc": "All in One Tool for Hacking and Pentesting", "repo": "https://github.com/cracker911181/Cracker-Tool", "reqs": "python", "help_cmd": "python cracker.py"},
        "06": {"name": "TermuxCyberArmy", "desc": "Linux tools repository/toolkit", "repo": "https://github.com/Err0r-ICA/TermuxCyberArmy", "reqs": "bash", "help_cmd": "bash install.sh"},
        "07": {"name": "onex", "desc": "Hacking tool installer and package manager", "repo": "https://github.com/jackind424/onex", "reqs": "bash", "help_cmd": "bash onex.sh"},
        "08": {"name": "Venom-Tool-Installer", "desc": "Kali Linux hacking tools installer for Termux", "repo": "https://github.com/hackingmastert56/Venom-Tool-Installer", "reqs": "bash", "help_cmd": "bash venom.sh"},
        "09": {"name": "Black-Tool", "desc": "Install the tools and start Attacking", "repo": "https://github.com/mrprogrammer2938/Black-Tool", "reqs": "python", "help_cmd": "python black-tool.py"},
        "10": {"name": "Termux-Lazyscript", "desc": "Tool for Termux Beginner users", "repo": "https://github.com/TechnicalMujeeb/Termux-Lazyscript", "reqs": "python", "help_cmd": "python termux-lazyscript.py"},
    }
}
