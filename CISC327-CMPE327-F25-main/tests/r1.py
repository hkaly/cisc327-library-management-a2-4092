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

def test_add_book_valid_input():
    """Test adding a book with valid input."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    assert success == True
    assert "successfully added" in message

def test_add_book_invalid_isbn_too_short():
    """Test adding a book with ISBN too short."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "123456789", 5)
    assert success == False
    assert "13 digits" in message

def test_add_book_title_required():
    """Test adding a book with missing title."""
    success, message = add_book_to_catalog("", "Test Author", "1234567890124", 5)
    assert success == False
    assert "title" in message and "required" in message

def test_add_book_title_max_length():
    """Test adding a book with title exceeding 200 characters."""
    long_title = "a" * 201
    success, message = add_book_to_catalog(long_title, "Test Author", "1234567890125", 5)
    assert success == False
    assert "200 characters" in message

def test_add_book_isbn_with_non_digits():
    """Test adding a book with ISBN containing non-digit characters."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "123456789012a", 5)
    assert success == False
    assert "digits" in message

def test_add_book_total_copies_negative():
    """Test adding a book with negative total copies."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890126", -1)
    assert success == False
    assert "positive integer" in message

def test_add_book_author_exactly_100_chars():
    """Test adding a book with author exactly 100 characters."""
    author_100_chars = "a" * 100
    success, message = add_book_to_catalog("Test Book", author_100_chars, "1234567890127", 5)
    assert success == True
    assert "successfully added" in message
