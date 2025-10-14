Harsh Kalyani - 20274092 - Group 2

|Functional Requirement| Function Name | Implementation Status | What is Missing |
|---|---------------|------------------------|-----------------|
|R1| test_add_book_valid_input | complete | nothing missing |
|R1| test_add_book_invalid_isbn_too_short | complete | nothing missing |
|R1| test_add_book_title_required | complete | nothing missing |
|R1| test_add_book_title_max_length | complete | nothing missing |
|R1| test_add_book_isbn_with_non_digits | complete | nothing missing |
|R1| test_add_book_total_copies_negative | complete | nothing missing |
|R1| test_add_book_author_exactly_100_chars | complete | nothing missing |
|R2| test_catalog_route_accessible | complete | nothing missing |
|R2| test_catalog_displays_heading | complete | nothing missing |
|R2| test_catalog_displays_table_with_books | complete | nothing missing |
|R2| test_catalog_table_headers_present | complete | nothing missing |
|R3| test_borrow_book_valid_input | partial | library_service.py helper function borrow_book_by_patron()|
|R3| test_borrow_book_patron_id_required | partial | library_service.py helper function borrow_book_by_patron()|
|R3| test_borrow_book_patron_id_too_short | partial | library_service.py helper function borrow_book_by_patron()|
|R3| test_borrow_book_invalid_book_id | partial | library_service.py helper function borrow_book_by_patron()|
|R3| test_borrow_book_no_copies_available | partial | library_service.py helper function borrow_book_by_patron()|
|R4| test_return_book_valid_input | partial | library_service.py helper function return_book_by_patron()|
|R4| test_return_book_patron_id_required | partial | library_service.py helper function return_book_by_patron()|
|R4| test_return_book_book_id_required | partial | library_service.py helper function return_book_by_patron()|
|R4| test_return_book_patron_id_too_short | partial | library_service.py helper function return_book_by_patron()|
|R4| test_return_book_patron_id_too_long | partial | library_service.py helper function return_book_by_patron()|
|R4| test_return_book_not_borrowed_by_patron | partial | library_service.py helper function return_book_by_patron()|
|R5| test_calculate_late_fee_valid_input | partial | library_service.py helper function calculate_late_fee_for_book()|
|R5| test_calculate_late_fee_1_day_overdue | partial | library_service.py helper function calculate_late_fee_for_book()|
|R5| test_calculate_late_fee_8_days_overdue | partial | library_service.py helper function calculate_late_fee_for_book()|
|R5| test_calculate_late_fee_14_days_overdue | partial | library_service.py helper function calculate_late_fee_for_book()|
|R5| test_calculate_late_fee_15_days_overdue | partial | library_service.py helper function calculate_late_fee_for_book()|
|R5| test_calculate_late_fee_exceeds_maximum | partial | library_service.py helper function calculate_late_fee_for_book()|
|R6| test_search_books_valid_title_search | partial | library_service.py helper function search_books_in_catalog()|
|R6| test_search_books_invalid_isbn_search | partial | library_service.py helper function search_books_in_catalog()|
|R6| test_search_books_title_partial_matching | partial | library_service.py helper function search_books_in_catalog()|
|R6| test_search_books_title_case_insensitive | partial | library_service.py helper function search_books_in_catalog()|
|R7| test_get_patron_status_valid_input | partial | library_service.py helper function get_patron_status_report()|
|R7| test_get_patron_status_patron_id_too_short | partial | library_service.py helper function get_patron_status_report()|
|R7| test_get_patron_status_patron_id_too_long | partial | library_service.py helper function get_patron_status_report()|
|R7| test_get_patron_status_patron_id_non_digits | partial | library_service.py helper function get_patron_status_report()|
|R7| test_get_patron_status_no_borrowed_books | partial | library_service.py helper function get_patron_status_report()|
|R7| test_get_patron_status_multiple_overdue_books | partial | library_service.py helper function get_patron_status_report()|