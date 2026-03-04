# Adding Tools to Tool-X

Tool-X uses a JSON based tool database.

All tools are stored inside:

core/tools.json

---

## Tool Format

Each tool entry follows this structure:

```json
"name": "ToolName",
"desc": "Tool description",
"repo": "https://github.com/example/tool
",
"reqs": "bash",
"help_cmd": "ls"
```
---

## Example Tool Entry
```json
"21": {
"name": "ExampleTool",
"desc": "Example OSINT tool",
"repo": "https://github.com/example/tool
",
"reqs": "python",
"help_cmd": "python tool.py"

}
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

1 Open:core/tools.json

2 Select a category

3 Add a new tool entry

4 Test installation

5 Submit Pull Request

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














