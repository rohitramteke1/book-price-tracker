import pytest
from scrape import scrape_all_books_paginated

def test_scraped_prices_are_positive():
    books = scrape_all_books_paginated()
    for book in books:
        assert book["price"] is not None, "Price should not be None"
        assert isinstance(book["price"], float), "Price should be a float"
        assert book["price"] > 0, "Price should be positive"

def test_titles_are_non_empty():
    books = scrape_all_books_paginated()
    for book in books:
        assert isinstance(book["title"], str), "Title should be a string"
        assert book["title"].strip() != '', "Title should not be empty" 