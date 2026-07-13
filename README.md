# AI-Assisted Programming Assessment: Library Management System
This repository contains the source code, documentation, and UML diagrams for the "Analyzing the Role of AI-Assisted Programming in Modern Software Development" assessment.
## Project Overview
The project involves implementing a **Library Management System** of moderate complexity using two distinct development approaches to evaluate the impact of AI in software engineering.
1. **Version A (Traditional Approach)**
   - Located in the `Version_A_Traditional/` directory.
   - Built entirely manually without AI assistance.
   - Uses procedural Python programming and saves data in-memory using JSON/text files.
   - Demonstrates a baseline level of development speed, code structure, and error handling.
2. **Version B (AI-Assisted Approach)**
   - Located in the `Version_B_AIAssisted/` directory.
   - Developed with the assistance of Large Language Models (LLMs) acting as intelligent co-pilots.
   - Employs Object-Oriented Programming (OOP) principles.
   - Utilizes a robust SQLite database for ACID-compliant storage.
   - Includes advanced features like error logging, input validation, and database constraint handling.
   - The AI prompts used during development are documented in `prompts.md` within this directory.
## Repository Contents
- `Version_A_Traditional/` - Source code for the manual implementation.
- `Version_B_AIAssisted/` - Source code and prompt logs for the AI-assisted implementation.
- `Assessment_Report.docx` - The final compiled assessment report containing conceptual analysis, comparative evaluation, and critical analysis of the AI tools.
- `generate_report.py` - The Python script used to automatically construct and format the Word document and download the UML diagrams.
- `*.png` - Generated UML diagrams (Use Case, Class, Activity, Sequence) visually describing the system architecture and logic.
## How to Run
### Requirements
- Python 3.x
- `sqlite3` (built into Python standard library)
### Running Version A
```bash
cd Version_A_Traditional
python library_system.py
```
### Running Version B
```bash
cd Version_B_AIAssisted
python library_system_ai.py
```
## UML Diagrams
The UML diagrams were automatically generated and saved in the root directory. They provide a clear representation of the system's requirements, structure, and dynamic behaviors.

