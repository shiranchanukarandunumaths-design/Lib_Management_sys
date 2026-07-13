import json
import os
import datetime

# Global lists to act as our database
books = []
users = []
transactions = []

BOOKS_FILE = "books.json"
USERS_FILE = "users.json"
TRANS_FILE = "transactions.json"

def load_data():
    global books, users, transactions
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, 'r') as f:
            books = json.load(f)
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
    if os.path.exists(TRANS_FILE):
        with open(TRANS_FILE, 'r') as f:
            transactions = json.load(f)

def save_data():
    with open(BOOKS_FILE, 'w') as f:
        json.dump(books, f, indent=4)
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)
    with open(TRANS_FILE, 'w') as f:
        json.dump(transactions, f, indent=4)

def add_book():
    print("--- Add a New Book ---")
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    isbn = input("Enter book ISBN: ")
    
    # Check if book exists
    for book in books:
        if book['isbn'] == isbn:
            print("Error: A book with this ISBN already exists.")
            return

    new_book = {
        'id': len(books) + 1,
        'title': title,
        'author': author,
        'isbn': isbn,
        'is_borrowed': False
    }
    books.append(new_book)
    save_data()
    print("Book added successfully!")

def register_user():
    print("--- Register New User ---")
    name = input("Enter user name: ")
    email = input("Enter user email: ")

    new_user = {
        'id': len(users) + 1,
        'name': name,
        'email': email
    }
    users.append(new_user)
    save_data()
    print("User registered successfully!")

def view_books():
    print("--- Library Books ---")
    if not books:
        print("No books available.")
        return
    for book in books:
        status = "Borrowed" if book['is_borrowed'] else "Available"
        print(f"ID: {book['id']} | Title: {book['title']} | Author: {book['author']} | Status: {status}")

def borrow_book():
    print("--- Borrow a Book ---")
    user_id = input("Enter User ID: ")
    book_id = input("Enter Book ID: ")

    # Basic error handling
    try:
        user_id = int(user_id)
        book_id = int(book_id)
    except ValueError:
        print("Error: IDs must be numbers.")
        return

    # Find user
    user_found = False
    for user in users:
        if user['id'] == user_id:
            user_found = True
            break
    if not user_found:
        print("Error: User not found.")
        return

    # Find book
    book_found = None
    for book in books:
        if book['id'] == book_id:
            book_found = book
            break
    
    if not book_found:
        print("Error: Book not found.")
        return

    if book_found['is_borrowed']:
        print("Error: Book is already borrowed.")
        return

    # Borrow process
    book_found['is_borrowed'] = True
    transaction = {
        'user_id': user_id,
        'book_id': book_id,
        'borrow_date': str(datetime.date.today()),
        'return_date': None
    }
    transactions.append(transaction)
    save_data()
    print("Book borrowed successfully!")

def return_book():
    print("--- Return a Book ---")
    book_id = input("Enter Book ID: ")
    
    try:
        book_id = int(book_id)
    except ValueError:
        print("Error: Book ID must be a number.")
        return

    # Find book
    book_found = None
    for book in books:
        if book['id'] == book_id:
            book_found = book
            break
            
    if not book_found:
        print("Error: Book not found.")
        return
        
    if not book_found['is_borrowed']:
        print("Error: Book is not currently borrowed.")
        return

    book_found['is_borrowed'] = False
    
    # Update transaction
    for trans in reversed(transactions):
        if trans['book_id'] == book_id and trans['return_date'] is None:
            trans['return_date'] = str(datetime.date.today())
            break
            
    save_data()
    print("Book returned successfully!")

def main():
    load_data()
    while True:
        print("\n=== Library Management System (Traditional) ===")
        print("1. Add Book")
        print("2. Register User")
        print("3. View Books")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. Exit")
        
        choice = input("Select an option (1-6): ")
        
        if choice == '1':
            add_book()
        elif choice == '2':
            register_user()
        elif choice == '3':
            view_books()
        elif choice == '4':
            borrow_book()
        elif choice == '5':
            return_book()
        elif choice == '6':
            print("Exiting application...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
