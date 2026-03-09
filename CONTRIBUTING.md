# Contributing to Tool-X
![Contribute](https://img.shields.io/badge/Contribute-Guide-green)

Thank you for your interest in contributing to Tool-X.

Tool-X is an open-source framework designed to simplify the installation and management of cybersecurity and OSINT tools.

We welcome developers, security researchers, and contributors from all skill levels.

---

# Ways to Contribute

You can contribute in several ways:

• Add new tools to the database (`core/data.json`)
• Improve the CLI interface (`tool-x.py`)
• Fix bugs  
• Improve documentation  
• Improve installation scripts (`core/installation_logic.py`)
• Suggest new features  

---

# Development Setup

Clone the repository:
```bash
git clone [https://github.com/trmxvibs/Tool-X](https://github.com/trmxvibs/Tool-X)
cd Tool-X
bash setup.sh
```
---
# Run the framework:
```bash
toolx
```
(Or run python tool-x.py manually)
---

# Adding New Tools
All tools are stored inside: `core/data.json`

- Example format:
```json
"ExampleTool": {
    "name": "ExampleTool",
    "desc": "Example tool description",
    "category": ["osint", "information_gathering"],
    "url": "[https://github.com/example/tool.git](https://github.com/example/tool.git)",
    "package_manager": "git",
    "dependency": ["python", "bash"],
    "os": ["linux", "termux", "macos"]
}
```
## Make sure:
 - • GitHub repository works (No dead links)
- • Dependencies are correct
- • Description is clear

---




# Pull Request Guidelines
Before submitting a pull request:

- Test the tool installation locally
- Follow the existing JSON structure carefully
- Keep commit messages clear

## Example commit message:
- Added OSINT tool "ExampleTool"










