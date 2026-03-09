# Adding Tools to Tool-X

Tool-X uses a JSON based tool database.

All tools are stored inside:

`core/data.json`

---

## Tool Format

Each tool entry follows this structure:

```json
"ToolName": {
    "name": "ToolName",
    "desc": "Short description of the tool",
    "category": ["web_hacking", "osint"],
    "url": "[https://github.com/example/tool.git](https://github.com/example/tool.git)",
    "package_manager": "git",
    "dependency": ["python", "bash", "git"],
    "os": ["linux", "termux", "macos"]
}
```
---

## Example Tool Entry
```json
"seeker": {
        "name": "seeker",
        "desc": "Accurately Locate Smartphones using Social Engineering.",
        "url": "https://github.com/thewhiteh4t/seeker",
        "category": [
            "Social Engineering & Phishing"
        ],
        "dependency": [
            "bash"
        ],
        "package_manager": "git"
    },

```


---

## Fields Explanation

| Field | Description |
|------|-------------|
| name | Tool name |
| desc | Short description |
| repo | GitHub repository |
| reqs | Required dependencies |
| help_cmd | Command to run tool |

---

## Steps to Add a Tool

1. Open:`core/data.json`
2. Select a category
3. Add a new tool entry
4. Test installation
5. Submit Pull Request

---

## Testing

Run Tool-X
```sh
toolx
```

Navigate to the category and install the tool.

---

## Guidelines

• Ensure GitHub repo works  
• Provide correct dependencies  
• Keep descriptions short  
• Test installation before submitting














