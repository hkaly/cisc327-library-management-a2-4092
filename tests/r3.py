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

def test_borrow_book_valid_input():
    """Test borrowing a book with valid patron ID and book ID."""
    # Add a book to catalog and get its ID
    add_book_to_catalog("Python Programming", "John Smith", "1234567890300", 3)
    book = database.get_book_by_isbn("1234567890300")
    success, message = borrow_book_by_patron("123456", str(book['id']))
    assert success == True
    assert "successfully borrowed" in message


def test_borrow_book_patron_id_required():
    """Test borrowing a book with missing patron ID."""
    # Add a book to catalog and get its ID
    add_book_to_catalog("Java Basics", "Jane Doe", "1234567890301", 2)
    book = database.get_book_by_isbn("1234567890301")
    success, message = borrow_book_by_patron("", str(book['id']))
    assert success == False
    assert "patron ID required" in message


def test_borrow_book_patron_id_too_short():
    """Test borrowing a book with patron ID too short."""
    # Add a book to catalog and get its ID
    add_book_to_catalog("Web Development", "Bob Johnson", "1234567890302", 5)
    book = database.get_book_by_isbn("1234567890302")
    success, message = borrow_book_by_patron("12345", str(book['id']))
    assert success == False
    assert "6-digit" in message

def test_borrow_book_invalid_book_id():
    """Test borrowing a book with non-existent book ID."""
    # Add a book but use invalid book ID for borrowing
    add_book_to_catalog("Database Design", "Alice Wilson", "1234567890303", 4)
    success, message = borrow_book_by_patron("123456", "99999")
    assert success == False
    assert "book not found" in message 

def test_borrow_book_no_copies_available():
    """Test borrowing a book with no available copies."""
    # Add a book with no available copies
    add_book_to_catalog("Machine Learning", "David Brown", "1234567890304", 0)
    book = database.get_book_by_isbn("1234567890304")
    success, message = borrow_book_by_patron("123456", str(book['id']))
    assert success == False
    assert "not available" in message