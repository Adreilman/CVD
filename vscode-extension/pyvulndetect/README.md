# PyVulnDetect — VS Code Extension

ML-powered Python vulnerability detector that scans your code directly in VS Code.

## Features

- **Inline diagnostics** — flags vulnerable code with yellow underlines, just like a linter
- **Popup notification** — shows vulnerability type and confidence score instantly
- **5 vulnerability classes detected:**
  - CWE-89: SQL Injection
  - CWE-502: Insecure Deserialization  
  - CWE-79: XSS
  - CWE-78: OS Command Injection
  - Safe (no vulnerability detected)

## Requirements

The extension requires the PyVulnDetect API server running locally.

**1. Clone the main repo:**
```bash
git clone https://github.com/your-username/CVD.git
cd CVD
```

**2. Set up and run the API server:**
```bash
python -m venv venv
source venv/Scripts/activate   # Windows Git Bash
pip install -r requirements.txt
pip install fastapi uvicorn
uvicorn app.api:app --reload
```

## Usage

1. Make sure the API server is running at `http://127.0.0.1:8000`
2. Open any Python `.py` file in VS Code
3. Press `Ctrl+Shift+P`
4. Type `PyVulnDetect: Scan File` and hit Enter
5. Results appear as:
   - A popup notification in the bottom right
   - Yellow underline on the file if a vulnerability is detected (≥75% confidence)
   - Hover over the underline to see the vulnerability type

## How it works