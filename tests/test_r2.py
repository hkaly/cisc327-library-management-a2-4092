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

def test_catalog_route_accessible(client):
    """Test that /catalog route is accessible."""
    # Add a book to ensure catalog has content
    add_book_to_catalog("Python Programming", "John Smith", "1234567890200", 3)
    
    response = client.get('/catalog')
    assert response.status_code == 200


def test_catalog_displays_heading(client):
    """Test that catalog displays the correct heading."""
    # Add a book to ensure catalog has content
    add_book_to_catalog("Data Structures", "Jane Doe", "1234567890201", 2)
    
    response = client.get('/catalog')
    assert response.status_code == 200
    assert b'Book Catalog' in response.data


def test_catalog_displays_table_with_books(client):
    """Test that catalog displays table when books exist."""
    # Add a book to ensure table is displayed
    add_book_to_catalog("Web Development", "Bob Johnson", "1234567890202", 5)
    
    response = client.get('/catalog')
    assert response.status_code == 200
    response_text = response.data.decode('utf-8')
    assert '<table>' in response_text


def test_catalog_table_headers_present(client):
    """Test that all required table headers are present."""
    # Add a book to ensure table headers are displayed
    add_book_to_catalog("Database Design", "Alice Wilson", "1234567890203", 4)
    
    response = client.get('/catalog')
    assert response.status_code == 200
    response_text = response.data.decode('utf-8')
    
    assert '<table>' in response_text
    assert b'<th>ID</th>' in response.data
    assert b'<th>Title</th>' in response.data
    assert b'<th>Author</th>' in response.data
    assert b'<th>ISBN</th>' in response.data
    assert b'<th>Availability</th>' in response.data
    assert b'<th>Actions</th>' in response.data