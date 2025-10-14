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

def test_search_books_valid_title_search():
    """Test searching books with valid title search term."""
    # Add books with different titles for searching
    add_book_to_catalog("Python Programming", "John Smith", "1234567890600", 3)
    add_book_to_catalog("Java Programming", "Jane Doe", "1234567890601", 2)
    
    results = search_books_in_catalog("Python", "title")
    assert isinstance(results, list)
    assert len(results) >= 1

def test_search_books_invalid_isbn_search():
    """Test searching books with invalid ISBN search term."""
    # Add a book with specific ISBN for searching
    add_book_to_catalog("Machine Learning", "David Brown", "1234567890604", 3)
    
    results = search_books_in_catalog("0000567890604", "isbn")
    assert isinstance(results, list)
    assert len(results) == 0

def test_search_books_title_partial_matching():
    """Test partial matching for title searches."""
    # Add books with titles containing "Program"
    add_book_to_catalog("Advanced Programming", "Carol White", "1234567890605", 2)
    add_book_to_catalog("Program Design", "Mark Davis", "1234567890606", 3)
    
    results = search_books_in_catalog("Program", "title")
    assert isinstance(results, list)
    assert len(results) >= 2

def test_search_books_title_case_insensitive():
    """Test case insensitive search for titles."""
    # Add a book with specific title
    add_book_to_catalog("Software Engineering", "Tom Wilson", "1234567890609", 2)
    
    results_lower = search_books_in_catalog("software", "title")
    results_upper = search_books_in_catalog("SOFTWARE", "title")
    
    assert isinstance(results_lower, list)
    assert isinstance(results_upper, list)
    assert len(results_lower) == len(results_upper)
    assert len(results_lower) >= 2