import sqlite3
import datetime
import logging
from typing import Optional, List, Tuple

# Set up basic logging to track errors
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseManager:
    """Handles all database interactions."""
    def __init__(self, db_name: str = "library.db"):
        self.db_name = db_name
        self.initialize_database()

    def _execute_query(self, query: str, parameters: tuple = ()) -> sqlite3.Cursor:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            conn.commit()
            return cursor
            
    def _fetch_all(self, query: str, parameters: tuple = ()) -> List[tuple]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            return cursor.fetchall()
            
    def _fetch_one(self, query: str, parameters: tuple = ()) -> Optional[tuple]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            return cursor.fetchone()

    def initialize_database(self):
        """Creates necessary tables if they do not exist."""
        try:
            self._execute_query('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL
                )
            ''')
            self._execute_query('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    isbn TEXT UNIQUE NOT NULL,
                    is_borrowed BOOLEAN NOT NULL DEFAULT 0
                )
            ''')
            self._execute_query('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    book_id INTEGER,
                    borrow_date DATE,
                    return_date DATE,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(book_id) REFERENCES books(id)
                )
            ''')
            logging.info("Database initialized successfully.")
        except sqlite3.Error as e:
            logging.error(f"Database initialization failed: {e}")

class Library:
    """Core library management logic."""
    def __init__(self, db: DatabaseManager):
        self.db = db

    def add_book(self, title: str, author: str, isbn: str) -> bool:
        try:
            self.db._execute_query("INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)", (title, author, isbn))
            logging.info(f"Book added: {title}")
            return True
        except sqlite3.IntegrityError:
            logging.warning("Book with this ISBN already exists.")
            return False

    def register_user(self, name: str, email: str) -> bool:
        try:
            self.db._execute_query("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
            logging.info(f"User registered: {name}")
            return True
        except sqlite3.IntegrityError:
            logging.warning("User with this email already exists.")
            return False

    def get_all_books(self) -> List[tuple]:
        return self.db._fetch_all("SELECT id, title, author, isbn, is_borrowed FROM books")

    def borrow_book(self, user_id: int, book_id: int) -> bool:
        # Check if user exists
        if not self.db._fetch_one("SELECT id FROM users WHERE id = ?", (user_id,)):
            logging.warning("User ID not found.")
            return False

        # Check if book is available
        book = self.db._fetch_one("SELECT is_borrowed FROM books WHERE id = ?", (book_id,))
        if not book:
            logging.warning("Book ID not found.")
            return False
        if book[0] == 1:
            logging.warning("Book is currently borrowed.")
            return False

        # Execute transaction
        today = datetime.date.today().isoformat()
        try:
            self.db._execute_query("UPDATE books SET is_borrowed = 1 WHERE id = ?", (book_id,))
            self.db._execute_query("INSERT INTO transactions (user_id, book_id, borrow_date) VALUES (?, ?, ?)", 
                                  (user_id, book_id, today))
            logging.info(f"Book {book_id} borrowed by User {user_id}")
            return True
        except sqlite3.Error as e:
            logging.error(f"Borrow transaction failed: {e}")
            return False

    def return_book(self, book_id: int) -> bool:
        # Check if book is borrowed
        book = self.db._fetch_one("SELECT is_borrowed FROM books WHERE id = ?", (book_id,))
        if not book:
            logging.warning("Book ID not found.")
            return False
        if book[0] == 0:
            logging.warning("Book is not currently borrowed.")
            return False

        today = datetime.date.today().isoformat()
        try:
            self.db._execute_query("UPDATE books SET is_borrowed = 0 WHERE id = ?", (book_id,))
            self.db._execute_query('''
                UPDATE transactions 
                SET return_date = ? 
                WHERE book_id = ? AND return_date IS NULL
            ''', (today, book_id))
            logging.info(f"Book {book_id} returned.")
            return True
        except sqlite3.Error as e:
            logging.error(f"Return transaction failed: {e}")
            return False

def main_menu():
    db_manager = DatabaseManager()
    library = Library(db_manager)

    while True:
        print("\n=== Library Management System (AI-Assisted) ===")
        print("1. Add Book")
        print("2. Register User")
        print("3. View Books")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. Exit")

        choice = input("Select an option (1-6): ").strip()

        if choice == '1':
            title = input("Title: ")
            author = input("Author: ")
            isbn = input("ISBN: ")
            if library.add_book(title, author, isbn):
                print("Success: Book added.")
            else:
                print("Error: Could not add book (duplicate ISBN).")

        elif choice == '2':
            name = input("Name: ")
            email = input("Email: ")
            if library.register_user(name, email):
                print("Success: User registered.")
            else:
                print("Error: Could not register user (duplicate Email).")

        elif choice == '3':
            books = library.get_all_books()
            if not books:
                print("No books in library.")
            else:
                print("\nID | Title | Author | ISBN | Status")
                print("-" * 50)
                for b in books:
                    status = "Borrowed" if b[4] else "Available"
                    print(f"{b[0]} | {b[1]} | {b[2]} | {b[3]} | {status}")

        elif choice == '4':
            try:
                user_id = int(input("User ID: "))
                book_id = int(input("Book ID: "))
                if library.borrow_book(user_id, book_id):
                    print("Success: Book borrowed.")
                else:
                    print("Error: Could not borrow book. Check User/Book ID or availability.")
            except ValueError:
                print("Error: IDs must be integers.")

        elif choice == '5':
            try:
                book_id = int(input("Book ID: "))
                if library.return_book(book_id):
                    print("Success: Book returned.")
                else:
                    print("Error: Could not return book. Check Book ID or status.")
            except ValueError:
                print("Error: IDs must be integers.")

        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main_menu()
