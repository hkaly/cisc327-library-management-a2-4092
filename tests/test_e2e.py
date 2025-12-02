from playwright.sync_api import Page, expect
import random, database

BASE_URL = "http://localhost:5000" #containerized on docker port 5000

def add_book_to_catalog_and_borrow(page: Page):
    # ADD BOOK
    # Go to route
    page.goto(BASE_URL +"/add_book")

    # Fill form to add book 
    page.fill("input[name='title']", "PLAYWRIGHT")
    page.fill("input[name='author']", "ME")
    page.fill("input[name='isbn']", 1312111098765)
    page.fill("input[name='total_copies']", "3")

    # Submit form
    page.click("text=Add Book to Catalog")

    # Wait for redirect to catalog route
    page.wait_for_url(BASE_URL + "/catalog")

    # Book should appear in catalog table
    row = page.get_by_role("row").filter(has_text=1312111098765)
    expect(row).to_be_visible()
    expect(row.get_by_role("cell", name="PLAYWRIGHT")).to_be_visible()
    expect(row.get_by_role("cell", name="ME")).to_be_visible()

    # BORROW
    patron = "996699" 

    # Enter patron ID in row
    row.locator("input[name='patron_id']").fill(patron)

    # Submit form 
    row.get_by_role("button", name="Borrow").click()
    
    # Get verification message
    expect(page.get_by_text("Successfully borrowed \"PLAYWRIGHT\"")).to_be_visible()