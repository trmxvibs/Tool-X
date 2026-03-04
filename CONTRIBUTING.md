# Contributing to Tool-X

Thank you for your interest in contributing to Tool-X.

Tool-X is an open-source framework designed to simplify the installation and management of cybersecurity and OSINT tools.

We welcome developers, security researchers, and contributors from all skill levels.

---

# Ways to Contribute

You can contribute in several ways:

• Add new tools to the database  
• Improve the CLI interface  
• Fix bugs  
• Improve documentation  
• Improve installation scripts  
• Suggest new features  

---

# Development Setup

Clone the repository:
```python
git clone https://github.com/trmxvibs/Tool-X

cd Tool-X

bash setup.sh
```
# Run the framework
```sh
python tool-x.py
```

---

# Adding New Tools

All tools are stored inside:
core/tools.json
Example format:

```json
{
"name": "ExampleTool",
"desc": "Example tool description",
"repo": "https://github.com/example/tool
",
"reqs": "bash",
"help_cmd": "ls"
}
```

## Make sure:

• GitHub repository works  
• Dependencies are correct  
• Description is clear  

---

# Pull Request Guidelines

Before submitting a pull request:

• Test the tool installation  
• Follow the existing JSON structure  
• Keep commit messages clear  

## Example commit message:
`Added OSINT tool "ExampleTool"`

---

# Reporting Issues

If you encounter a bug:

Open an issue on GitHub and include:

• Tool name  
• Error message  
• System information  

---

# Community

You can support the project by:

⭐ Starring the repository  
🍴 Forking the project  
🐞 Reporting bugs  
🚀 Submitting pull requests  

---

Thank you for helping improve Tool-X.
















