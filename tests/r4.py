import pytest, json, database
from datetime import datetime, timedelta
from library_service import (
    add_book_to_catalog,
    borrow_book_by_patron,
    return_book_by_patron,
    calculate_late_fee_for_book,
    search_books_in_catalog,
    get_patron_status_report
)

def test_return_book_valid_input():
    """Test returning a book with valid patron ID and book ID."""
    # Add a book and borrow it first
    add_book_to_catalog("Python Programming", "John Smith", "1234567890400", 3)
    book = database.get_book_by_isbn("1234567890400")
    
    # First borrow the book
    borrow_book_by_patron("123456", str(book['id']))
    
    # Then try to return it
    success, message = return_book_by_patron("123456", str(book['id']))
    assert success == True
    assert "successfully returned" in message


def test_return_book_patron_id_required():
    """Test returning a book with missing patron ID."""
    # Add a book and borrow it first
    add_book_to_catalog("Java Basics", "Jane Doe", "1234567890401", 2)
    book = database.get_book_by_isbn("1234567890401")
    
    # First borrow the book
    borrow_book_by_patron("123456", str(book['id']))
    
    # Try to return with empty patron ID
    success, message = return_book_by_patron("", str(book['id']))
    assert success == False
    assert "patron ID required" in message


def test_return_book_book_id_required():
    """Test returning a book with missing book ID."""
    # Add a book and borrow it first
    add_book_to_catalog("Web Development", "Bob Johnson", "1234567890402", 5)
    book = database.get_book_by_isbn("1234567890402")
    
    # First borrow the book
    borrow_book_by_patron("123456", str(book['id']))
    
    # Try to return with empty book ID
    success, message = return_book_by_patron("123456", "")
    assert success == False
    assert "book ID required" in message


def test_return_book_patron_id_too_short():
    """Test returning a book with patron ID too short."""
    # Add a book and borrow it first
    add_book_to_catalog("Database Design", "Alice Wilson", "1234567890403", 4)
    book = database.get_book_by_isbn("1234567890403")
    
    # First borrow the book with valid patron ID
    borrow_book_by_patron("123456", str(book['id']))
    
    # Try to return with short patron ID
    success, message = return_book_by_patron("12345", str(book['id']))
    assert success == False
    assert "6-digit" in message


def test_return_book_patron_id_too_long():
    """Test returning a book with patron ID too long."""
    # Add a book and borrow it first
    add_book_to_catalog("Machine Learning", "David Brown", "1234567890404", 3)
    book = database.get_book_by_isbn("1234567890404")
    
    # First borrow the book with valid patron ID
    borrow_book_by_patron("123456", str(book['id']))
    # Try to return with long patron ID
    success, message = return_book_by_patron("1234567", str(book['id']))
    assert success == False
    assert "6-digit" in message


def test_return_book_not_borrowed_by_patron():
    """Test returning a book that was not borrowed by the patron."""
    # Add a book but don't borrow it
    add_book_to_catalog("Data Structures", "Carol White", "1234567890405", 2)
    book = database.get_book_by_isbn("1234567890405")

    # Try to return without borrowing first
    success, message = return_book_by_patron("123456", str(book['id']))
    assert success == False
    assert "not borrowed" in message