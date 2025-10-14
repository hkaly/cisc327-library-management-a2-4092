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

def test_get_patron_status_valid_input():
    """Test getting patron status with valid patron ID."""
    # Add books and create borrowing scenario
    add_book_to_catalog("Python Programming", "John Smith", "1234567890700", 3)
    add_book_to_catalog("Java Basics", "Jane Doe", "1234567890701", 2)
    book1 = database.get_book_by_isbn("1234567890700")
    book2 = database.get_book_by_isbn("1234567890701")
    
    # Borrow books
    borrow_book_by_patron("123456", str(book1['id']))
    borrow_book_by_patron("123456", str(book2['id']))
    
    success, report = get_patron_status_report("123456")
    assert success == True
    assert isinstance(report, dict)

def test_get_patron_status_patron_id_too_short():
    """Test patron status with patron ID too short."""
    success, report = get_patron_status_report("12345")
    assert success == False
    assert "6-digit" in report

def test_get_patron_status_patron_id_too_long():
    """Test patron status with patron ID too long."""
    success, report = get_patron_status_report("1234567")
    assert success == False
    assert "6-digit" in report

def test_get_patron_status_patron_id_non_digits():
    """Test patron status with patron ID containing non-digits."""
    success, report = get_patron_status_report("12345a")
    assert success == False
    assert "6-digit" in report

def test_get_patron_status_no_borrowed_books():
    """Test patron status for patron with no currently borrowed books."""
    # Add a book but don't borrow it
    add_book_to_catalog("Network Security", "Sarah Thompson", "1234567890708", 5)
    
    success, report = get_patron_status_report("111111")
    assert success == True
    assert "currently_borrowed" in report
    assert len(report["currently_borrowed"]) == 0
    assert "books_borrowed_count" in report
    assert report["books_borrowed_count"] == 0

def test_get_patron_status_multiple_overdue_books():
    """Test patron status with multiple overdue books calculates total fees."""
    # Add multiple books and simulate overdue scenarios
    add_book_to_catalog("Mobile Development", "Helen Rodriguez", "1234567890712", 3)
    add_book_to_catalog("Cloud Computing", "James Taylor", "1234567890713", 2)
    book1 = database.get_book_by_isbn("1234567890712")
    book2 = database.get_book_by_isbn("1234567890713")
    
    # Simulate overdue borrowings
    borrow_date1 = datetime.now() - timedelta(days=16)  # 2 days overdue
    due_date1 = borrow_date1 + timedelta(days=14)
    database.update_book_availability(book1['id'], -1)
    database.insert_borrow_record("123456", book1['id'], borrow_date1, due_date1)
    
    borrow_date2 = datetime.now() - timedelta(days=18)  # 4 days overdue
    due_date2 = borrow_date2 + timedelta(days=14)
    database.update_book_availability(book2['id'], -1)
    database.insert_borrow_record("123456", book2['id'], borrow_date2, due_date2)
    
    success, report = get_patron_status_report("123456")
    assert success == True
    assert "total_late_fees" in report
    assert report["total_late_fees"] > 0