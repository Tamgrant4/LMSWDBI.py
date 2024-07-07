import mysql.connector

def connect_to_db():
  """Connects to the MySQL database."""
  conn = mysql.connector.connect(
      host="localhost",
      user="your_username",
      password="your_password",
      database="library_management"
  )
  return conn

def add_book(title, author_id, genre_id, isbn, publication_date):
  """Adds a new book to the database."""
  conn = connect_to_db()
  cursor = conn.cursor()
  sql = """
      INSERT INTO books (title, author_id, genre_id, isbn, publication_date)
      VALUES (%s, %s, %s, %s, %s)
  """
  cursor.execute(sql, (title, author_id, genre_id, isbn, publication_date))
  conn.commit()
  print("Book added successfully!")
  conn.close()

def borrow_book(book_id, user_id):
  """Borrows a book by updating its availability and creating a borrow record."""
  conn = connect_to_db()
  cursor = conn.cursor()
  # Check book availability first
  cursor.execute("SELECT availability FROM books WHERE id = %s", (book_id,))
  available = cursor.fetchone()[0]
  if not available:
    print("Book is not currently available.")
    return
  # Update book availability
  cursor.execute("UPDATE books SET availability = 0 WHERE id = %s", (book_id,))
  # Create borrow record
  cursor.execute("""
      INSERT INTO borrowed_books (user_id, book_id, borrow_date)
      VALUES (%s, %s, CURDATE())
  """, (user_id, book_id))
  conn.commit()
  print("Book borrowed successfully!")
  conn.close()

def return_book(book_id):
  """Returns a book by updating its availability and deleting the borrow record."""
  conn = connect_to_db()
  cursor = conn.cursor()
  # Update book availability
  cursor.execute("UPDATE books SET availability = 1 WHERE id = %s", (book_id,))
  # Delete borrow record
  cursor.execute("DELETE FROM borrowed_books WHERE book_id = %s", (book_id,))
  conn.commit()
  print("Book returned successfully!")
  conn.close()

def search_books(search_term):
  """Searches for books by title, author, or ISBN."""
  conn = connect_to_db()
  cursor = conn.cursor()
  sql = """
      SELECT * FROM books
      WHERE title LIKE %s OR authors.name LIKE %s OR isbn = %s
  """
  cursor.execute(sql, ("%" + search_term + "%", "%" + search_term + "%", search_term))
  results = cursor.fetchall()
  if not results:
    print("No books found matching your search criteria.")
  else:
    print("Search results:")
    for book in results:
      print(f"- {book[1]} (by {book[2]})")  # Display title and author
  conn.close()

def list_books():
  """Displays a list of all books."""
  conn = connect_to_db()
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM books")
  results = cursor.fetchall()
  if not results:
    print("There are no books in the library.")
  else:
    print("List of all books:")
    for book in results:
      print(f"- {book[1]} (by {book[2]})")  # Display title and author
  conn.close()


