# Tool-X Framework Architecture

Tool-X is designed as a modular CLI framework.

The system consists of four main components.

---

## 1. CLI Engine

File:tool-x.py

Responsibilities:

- Interactive terminal dashboard  
- Tool search system  
- Favorites manager  
- Pagination system  
- Category navigation  
This file acts as the main controller of the entire framework.
---

## 2. Installation Engine

File:core/installation_logic.py

Responsibilities:

- Install tools from GitHub  
- Clone repositories  
- Install dependencies  
- Handle errors and logs  

All tool installation logic is centralized here.

---

## 3. Tool Database Loader

File:core/tool_data.py

Responsibilities:

- Load tools.json database  
- Parse categories  
- Provide structured data to CLI engine

This allows the framework to scale easily.

---

## 4. Tool Database

File:

core/tools.json

Contains:

- tool name  
- description  
- GitHub repository  
- dependencies  
- help commands  

Because tools are stored in JSON format, adding new tools requires **no Python code modification**.

---

## Data Flow

- tools.json
     ↓
- tool_data.py
     ↓
- tool-x.py
     ↓
- installation_logic.py
     ↓
- GitHub tool installation
