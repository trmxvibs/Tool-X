# Tool-X Framework Architecture

Tool-X is designed as a modular CLI framework.

The system consists of four main components.

---

## 1. CLI Engine

**File:** `tool-x.py`

**Responsibilities:**
- Interactive terminal dashboard  
- Tool search system  
- Favorites manager  
- Pagination system  
- Category navigation  

This file acts as the main controller of the entire framework.

---

## 2. Installation Engine

**File:** `core/installation_logic.py`

**Responsibilities:**
- Install tools from GitHub or via Curl
- Clone repositories  
- Install dependencies automatically
- Universal OS Compatibility Check (Termux, Linux, Windows, Mac)
- Handle errors and secure logging  

All tool installation logic is centralized here.

---

## 3. Tool Database Loader

**File:** `core/tool_data.py`

**Responsibilities:**
- Load `data.json` database  
- Parse and merge categories dynamically 
- Provide structured data and numeric IDs to the CLI engine

This allows the framework to scale easily to thousands of tools.

---

## 4. Tool Database

**File:** `core/data.json`

**Contains:**
- tool name  
- description  
- GitHub repository URL
- supported OS
- package manager
- dependencies  

Because tools are stored in JSON format, adding new tools requires **no Python code modification**.

---

## Data Flow

`data.json`

     ↓
     
`core/tool_data.py`

     ↓
     
`tool-x.py`

     ↓

`core/installation_logic.py`

     ↓

`Tool Installation`
