<h1 align="center" style="color:##ffd300; text-decoration: underline;">Tool-X</h1>

## The Apex Termux Installation Framework

<p align="center">
  <img src="https://img.shields.io/github/stars/trmxvibs/Tool-X?style=for-the-badge&color=ffd300" alt="GitHub Stars">
  <img src="https://img.shields.io/github/forks/trmxvibs/Tool-X?style=for-the-badge&color=blueviolet" alt="GitHub Forks">
  <img src="https://img.shields.io/github/last-commit/trmxvibs/Tool-X?style=for-the-badge&color=9cf" alt="Last Commit">
  <img src="https://img.shields.io/badge/Status-ACTIVE-brightgreen?style=for-the-badge" alt="Project Status">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Tested%20On-Termux%20%7C%20Kali%20Nethunter-orange?style=flat&logo=android" alt="Tested On">
  <img src="https://img.shields.io/badge/Language-Python%203.x%20%7C%20Shell-blue?style=flat&logo=python" alt="Language">
  <img src="https://img.shields.io/badge/License-MIT-blue?style=flat" alt="License">
</p>


[![ShellCheck](https://github.com/trmxvibs/Tool-X/actions/workflows/shellcheck.yml/badge.svg)](https://github.com/trmxvibs/Tool-X/actions/workflows/shellcheck.yml)


---
## Overview

Tool-X is an installation and management framework designed to turn a Termux environment into a robust mobile penetration-testing toolkit. It automates dependency fixes, repository cloning, mirror adjustments, and common Termux issues so you can focus on using tools instead of installing them.


## Key Features
- One-step setup for 60+ commonly used tools.

- Termux-specific fixes (gem issues, Python library patches, CWD errors) included.

- Management utilities: search engine, status dashboard, selective uninstall, and self-update.
- ![Made in India](https://img.shields.io/badge/Made%20in-India-FF9933?style=for-the-badge&logo=india&logoColor=white)


## Installtion 
- **Copy Command and paste in terminal**

  ```python
  pkg install git wget -y && wget https://raw.githubusercontent.com/trmxvibs/Tool-X/main/setup.sh -O setup.sh && chmod +x setup.sh && ./setup.sh
  ```
  ## Note: Restart your Termux session after the script finishes to apply the toolx alias and environment changes.
  
### How to Launch & Core Menu Options

After restarting Termux, start the framework from any directory with:

## `toolx`

### Menu references inside Tool-X:

- [97] Search Tools — Find tools by keyword (e.g., osint, bruteforce).

- [94] View Status — Inspect installed tool paths and view error logs.

- [99] Self-Update — Update the framework (git pull).

 - [98] Clean Uninstall — Remove tracked tool directories selectively.

- [96] Self-Destruct — Remove the entire ~/tool-x directory and the global toolx alias.

## Maintenance & Troubleshooting

If a package fails: check mirror fixes included in the script.

Dependency issues: the setup will attempt to install Ruby, Python libraries, figlet, and other common dependencies.

Check logs: use the status option to read error logs and follow the suggested fixes.

## Usage Policy

Tool-X is provided for educational purposes and authorized penetration testing only. The project author (trmxvibs) is not responsible for misuse. Always have permission before testing systems that you do not own.

## Quick FAQ

Q: Why restart Termux?

A: Restarting ensures the toolx alias and any environment changes are loaded into the shell session.

Q: Setup failed — what now?

A: Run toolx and choose [94] View Status to examine logs. Common causes are network/mirror problems, missing git/wget, or permission errors.

## 📎 Repository & License

Official repo: https://github.com/trmxvibs/Tool-X

![Last Updated](https://img.shields.io/date/1731264000?label=Last%20Update&color=orange)





  
