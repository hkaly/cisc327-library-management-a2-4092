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

def test_calculate_late_fee_valid_input():
    """Test calculating late fee with valid patron ID and book ID."""
    # Add a book, borrow it, and simulate it being overdue
    add_book_to_catalog("Python Programming", "John Smith", "1234567890500", 3)
    book = database.get_book_by_isbn("1234567890500")
    
    # Borrow the book and simulate due date
    borrow_book_by_patron("123456", str(book['id']))
    
    success, response = calculate_late_fee_for_book("123456", str(book['id']))
    assert success == True
    response_data = json.loads(response)
    assert "fee_amount" in response_data
    assert "days_overdue" in response_data

def test_calculate_late_fee_1_day_overdue():
    """Test calculating late fee for book 1 day overdue."""
    # Add a book and simulate 1 day overdue
    add_book_to_catalog("Java Basics", "Jane Doe", "1234567890501", 2)
    book = database.get_book_by_isbn("1234567890501")
    
    # Simulate borrowing 15 days ago (1 day overdue from 14-day due period)
    borrow_date = datetime.now() - timedelta(days=15)
    due_date = borrow_date + timedelta(days=14)
    database.update_book_availability(book['id'], -1)
    database.insert_borrow_record("123456", book['id'], borrow_date, due_date)
    
    success, response = calculate_late_fee_for_book("123456", str(book['id']))
    assert success == True
    response_data = json.loads(response)
    assert response_data["fee_amount"] == 0.50
    assert response_data["days_overdue"] == 1

def test_calculate_late_fee_8_days_overdue():
    """Test calculating late fee for book 8 days overdue."""
    # Add a book and simulate 8 days overdue
    add_book_to_catalog("Web Development", "Bob Johnson", "1234567890502", 5)
    book = database.get_book_by_isbn("1234567890502")
    
    # Simulate borrowing 22 days ago (8 days overdue from 14-day due period)
    borrow_date = datetime.now() - timedelta(days=22)
    due_date = borrow_date + timedelta(days=14)
    database.update_book_availability(book['id'], -1)
    database.insert_borrow_record("123456", book['id'], borrow_date, due_date)
    
    success, response = calculate_late_fee_for_book("123456", str(book['id']))
    assert success == True
    response_data = json.loads(response)
    assert response_data["fee_amount"] == 4.50  # 7 * $0.50 + 1 * $1.00
    assert response_data["days_overdue"] == 8

def test_calculate_late_fee_14_days_overdue():
    """Test calculating late fee for book 14 days overdue."""
    # Add a book and simulate 14 days overdue
    add_book_to_catalog("Database Design", "Alice Wilson", "1234567890503", 4)
    book = database.get_book_by_isbn("1234567890503")
    
    # Simulate borrowing 28 days ago (14 days overdue from 14-day due period)
    borrow_date = datetime.now() - timedelta(days=28)
    due_date = borrow_date + timedelta(days=14)
    database.update_book_availability(book['id'], -1)
    database.insert_borrow_record("123456", book['id'], borrow_date, due_date)
    
    success, response = calculate_late_fee_for_book("123456", str(book['id']))
    assert success == True
    response_data = json.loads(response)
    assert response_data["fee_amount"] == 10.50  # 7 * $0.50 + 7 * $1.00
    assert response_data["days_overdue"] == 14

def test_calculate_late_fee_15_days_overdue():
    """Test calculating late fee for book 15 days overdue."""
    # Add a book and simulate 15 days overdue
    add_book_to_catalog("Machine Learning", "David Brown", "1234567890504", 3)
    book = database.get_book_by_isbn("1234567890504")
    
    # Simulate borrowing 29 days ago (15 days overdue from 14-day due period)
    borrow_date = datetime.now() - timedelta(days=29)
    due_date = borrow_date + timedelta(days=14)
    database.update_book_availability(book['id'], -1)
    database.insert_borrow_record("123456", book['id'], borrow_date, due_date)
    
    success, response = calculate_late_fee_for_book("123456", str(book['id']))
    assert success == True
    response_data = json.loads(response)
    assert response_data["fee_amount"] == 11.50  # 7 * $0.50 + 8 * $1.00
    assert response_data["days_overdue"] == 15

def test_calculate_late_fee_exceeds_maximum():
    """Test calculating late fee for book with very high overdue days."""
    # Add a book and simulate way overdue (should hit $15 maximum)
    add_book_to_catalog("Data Structures", "Carol White", "1234567890505", 2)
    book = database.get_book_by_isbn("1234567890505")
    
    # Simulate borrowing 50 days ago (36 days overdue from 14-day due period)
    borrow_date = datetime.now() - timedelta(days=50)
    due_date = borrow_date + timedelta(days=14)
    database.update_book_availability(book['id'], -1)
    database.insert_borrow_record("123456", book['id'], borrow_date, due_date)
    
    success, response = calculate_late_fee_for_book("123456", str(book['id']))
    assert success == True
    response_data = json.loads(response)
    assert response_data["fee_amount"] == 15.00  # Should be capped at $15
    assert response_data["days_overdue"] == 36