# AI Prompts used for Version B (AI-Assisted)

During the development of `Version_B_AIAssisted/library_system_ai.py`, the following prompts were used in a conversational AI tool (like ChatGPT or GitHub Copilot) to generate and refine the code.

## Prompt 1: Initial Architecture
**User:**
"Write a Python Library Management System that uses SQLite for the database. It should have tables for books, users, and transactions. Use Object-Oriented Programming principles. The library class should have methods to add books, register users, borrow books, and return books."

**AI Response:**
*(AI generated the basic structure of the `DatabaseManager` and `Library` classes, including table creation queries and basic insert methods.)*

## Prompt 2: Refinement - Error Handling
**User:**
"Enhance the previous code by adding robust error handling. Use Python's built-in `logging` module to log database errors (e.g., IntegrityError for duplicate ISBNs or emails). Also, ensure the borrow_book method checks if the user exists and if the book is already borrowed."

**AI Response:**
*(AI added the `logging` imports and implemented `try...except` blocks around SQL queries. It also added pre-checks for user and book existence before updating the database.)*

## Prompt 3: Refinement - CLI Interface
**User:**
"Now write a `main_menu` function that provides a Command Line Interface (CLI) for the library system. It should run in a loop and handle user inputs safely, catching ValueError if the user enters non-integers for IDs."

**AI Response:**
*(AI generated the `main_menu` loop, complete with `input()` prompts and `try...except ValueError` blocks to prevent crashes on bad input.)*
