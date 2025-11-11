import pytest
from services.library_service import pay_late_fees, refund_late_fee_payment
from services.payment_service import PaymentGateway
from unittest.mock import Mock, patch

#pay_late_fees tests

def test_successful_payment(mocker):
    """
    Test successful payment processing with valid patron and book
    """
    #Stubs
    mocker.patch(
        'services.library_service.calculate_late_fee_for_book',
        return_value={'fee_amount': 5.50, 'days_overdue': 11, 'status': 'Late fee calculated.'}
    )
    mocker.patch(
        'services.library_service.get_book_by_id',
        return_value={'book_id': 1, 'title': 'Test Book', 'author': 'Test Author'}
    )

    # Mock payment gateway
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_123456", "Payment successful")
    success, message, transaction_id = pay_late_fees("123456", 1, mock_gateway)

    assert success is True
    assert "Payment successful" in message
    assert transaction_id == "txn_123456"
    mock_gateway.process_payment.assert_called_once_with(
        patron_id="123456",
        amount=5.50,
        description="Late fees for 'Test Book'"
    )

def test_payment_declined_by_gateway(mocker):
    """
    Test payment declined scenario
    """
    mocker.patch(
        'services.library_service.calculate_late_fee_for_book',
        return_value={'fee_amount': 5.50, 'days_overdue': 11, 'status': 'Late fee calculated.'}
    )
    mocker.patch(
        'services.library_service.get_book_by_id',
        return_value={'book_id': 2, 'title': 'Test Book', 'author': 'Test Author'}
    )

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (False, None, "Card declined")
    success, message, transaction_id  = pay_late_fees("234567", 2, mock_gateway)
        
    assert success is False
    assert "Payment failed" in message
    assert transaction_id is None
    mock_gateway.process_payment.assert_called_once_with(
        patron_id="234567",
        amount=5.50,
        description="Late fees for 'Test Book'"
    )

def test_invalid_patron_id_payment_not_called(mocker):
    """
    Test invalid patron ID - payment gateway should NOT be called
    """
    mock_gateway = Mock(spec=PaymentGateway)
    invalid_id = "12345"
    success, message, transaction_id = pay_late_fees(invalid_id, 1, mock_gateway)
    assert success is False
    assert "Invalid patron ID" in message
    assert transaction_id is None
        
    # Verify payment gateway was NEVER called
    mock_gateway.process_payment.assert_not_called()

def test_zero_late_fees_payment_not_called(mocker):
    """
    Test zero late fees - payment gateway should NOT be called
    """
    mocker.patch(
        'services.library_service.calculate_late_fee_for_book',
        return_value={'fee_amount': 0.00, 'days_overdue': 0, 'status': 'Book is not overdue.'}
    )
    mocker.patch(
        'services.library_service.get_book_by_id',
        return_value={'book_id': 3, 'title': 'On Time Book', 'author': 'Punctual Author'}
    )
    mock_gateway = Mock(spec=PaymentGateway)
    success, message, transaction_id = pay_late_fees("345678", 3, mock_gateway)
    assert success is False
    assert "No late fees to pay" in message
    assert transaction_id is None
    mock_gateway.process_payment.assert_not_called()
    
def test_network_error_exception_handling(mocker):
    """
    Test network error exception 
    """
    mocker.patch(
        'services.library_service.calculate_late_fee_for_book',
        return_value={'fee_amount': 7.50, 'days_overdue': 15, 'status': 'Late fee calculated.'}
    )
    mocker.patch(
        'services.library_service.get_book_by_id',
        return_value={'book_id': 4, 'title': 'Network Test Book', 'author': 'Error Author'}
    )
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.side_effect = Exception("Network timeout")
    success, message, transaction_id = pay_late_fees("456789", 4, mock_gateway)
    assert success is False
    assert "Network timeout" in message
    assert transaction_id is None
    mock_gateway.process_payment.assert_called_once_with(
        patron_id="456789",
        amount=7.50,
        description="Late fees for 'Network Test Book'"
    )

#refund_late_fee_payment tests

def test_successful_refund(mocker):
    """
    Test successful refund processing
    """
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (True, "processed successfully")
    success, message = refund_late_fee_payment("txn_123456", 5.00, mock_gateway)
    assert success is True
    assert "processed successfully" in message
    mock_gateway.refund_payment.assert_called_once_with("txn_123456", 5.00)

def test_invalid_transaction_id_rejection(mocker):
    """
    Test invalid transaction ID - gateway NOT called
    """
    mock_gateway = Mock(spec=PaymentGateway)
    invalid_id = "invalid"
    success, message = refund_late_fee_payment(invalid_id, 5.00, mock_gateway)
    assert success is False
    assert "Invalid transaction ID" in message
    mock_gateway.refund_payment.assert_not_called()

def test_negative_refund_amount(mocker):
    """
    Test negative refund amount
    """
    mock_gateway = Mock(spec=PaymentGateway)
    success, message = refund_late_fee_payment("txn_123456", -5.00, mock_gateway)
    assert success is False
    assert "Refund amount must be greater than 0." in message
    mock_gateway.refund_payment.assert_not_called()
    
def test_zero_refund_amount(mocker):
    """
    Test zero refund amount
    """
    mock_gateway = Mock(spec=PaymentGateway)
    success, message = refund_late_fee_payment("txn_123456", 0.00, mock_gateway)
    assert success is False
    assert "Refund amount must be greater than 0." in message
    mock_gateway.refund_payment.assert_not_called()
    
def test_refund_exceeds_maximum(mocker):
    """
    Test refund amount exceeding $15 maximum
    """
    mock_gateway = Mock(spec=PaymentGateway)
    amount = 15.01
    success, message = refund_late_fee_payment("txn_123456", amount, mock_gateway)
    assert success is False
    assert "Refund amount exceeds maximum late fee." in message
    mock_gateway.refund_payment.assert_not_called()

#additional tests

def test_book_not_found_payment_not_called(mocker):
    """
    Test when book doesn't exist
    """
    mocker.patch(
        'services.library_service.calculate_late_fee_for_book',
        return_value={'fee_amount': 5.00, 'days_overdue': 10, 'status': 'Late fee calculated.'}
    )
    mocker.patch(
        'services.library_service.get_book_by_id',
        return_value=None  # Book not found
    )
    mock_gateway = Mock(spec=PaymentGateway)
    success, message, transaction_id = pay_late_fees("123456", 999, mock_gateway)
    assert success is False
    assert "Book not found" in message
    assert transaction_id is None
    mock_gateway.process_payment.assert_not_called()

def test_calculate_fee_returns_none(mocker):
    """
    Test when fee calculation fails and returns None
    """
    mocker.patch(
        'services.library_service.calculate_late_fee_for_book',
        return_value=None  # Calculation failed
    )
    
    mock_gateway = Mock(spec=PaymentGateway)
    success, message, transaction_id = pay_late_fees("123456", 1, mock_gateway)
    
    assert success is False
    assert "Unable to calculate late fees" in message
    assert transaction_id is None
    mock_gateway.process_payment.assert_not_called()

def test_missing_fee_amount_key(mocker):
    """
    Test when calculate_late_fee_for_book returns dict without fee_amount key
    """
    mocker.patch(
        'services.library_service.calculate_late_fee_for_book',
        return_value={'days_overdue': 5, 'status': 'Some status'}  # Missing fee_amount
    )
    
    mock_gateway = Mock(spec=PaymentGateway)
    success, message, transaction_id = pay_late_fees("123456", 1, mock_gateway)
    
    assert success is False
    mock_gateway.process_payment.assert_not_called()

def test_maximum_late_fee_payment(mocker):
    """
    Test payment with exactly maximum late fee ($15.00)
    """
    mocker.patch(
        'services.library_service.calculate_late_fee_for_book',
        return_value={'fee_amount': 15.00, 'days_overdue': 30, 'status': 'Late fee calculated.'}
    )
    mocker.patch(
        'services.library_service.get_book_by_id',
        return_value={'book_id': 13, 'title': 'Max Fee Book', 'author': 'Max Author'}
    )
    
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_max_fee", "Payment successful")
    success, message, transaction_id = pay_late_fees("444444", 13, mock_gateway)
    
    assert success is True
    assert transaction_id == "txn_max_fee"
    mock_gateway.process_payment.assert_called_once_with(
        patron_id="444444",
        amount=15.00,
        description="Late fees for 'Max Fee Book'"
    )

def test_refund_gateway_failure(mocker):
    """
    Test when payment gateway returns failure
    """
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (False, "Insufficient funds in merchant account")
    
    success, message = refund_late_fee_payment("txn_failed", 10.00, mock_gateway)
    
    assert success is False
    assert "Refund failed" in message
    assert "Insufficient funds in merchant account" in message
    mock_gateway.refund_payment.assert_called_once_with("txn_failed", 10.00)

def test_refund_exception_handling(mocker):
    """
    Test exception handling during refund processing
    """
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.side_effect = Exception("API timeout error")
    success, message = refund_late_fee_payment("txn_error", 8.00, mock_gateway)
        
    assert success is False
    assert "Refund processing error" in message
    assert "API timeout error" in message
    mock_gateway.refund_payment.assert_called_once_with("txn_error", 8.00)
    