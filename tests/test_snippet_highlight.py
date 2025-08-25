import pytest
import os

from snippet_highlight.snippet_highlight import highlight_doc, Snippet


@pytest.fixture
def basic_document():
    return "foo bar"


@pytest.fixture
def basic_query():
    return "bar"


@pytest.fixture
def long_document():
    with open("tests/test_document.txt") as f:
        return f.read()


@pytest.fixture
def long_query():
    return "George Lucas"


def highlight(text):
    return Snippet.HIGHLIGHT + text + Snippet.END_HIGHLIGHT


def test_highlight_doc_blank_doc_and_query():
    assert '' == highlight_doc('', '')


def test_highlight_doc_blank_query(basic_document):
    assert basic_document == highlight_doc(basic_document, '')


def test_highlight_doc_blank_doc(basic_query):
    assert '' == highlight_doc('', basic_query)


def test_highlight_doc(basic_document, basic_query):
    expected = "foo " + highlight("bar")
    assert expected == highlight_doc(basic_document, basic_query)


def test_highlight_doc_multiple_words(basic_document):
    expected = highlight(basic_document)
    assert expected == highlight_doc(basic_document, basic_document)


def test_highlight_doc_longer_query_than_doc(basic_document):
    expected = highlight(basic_document)
    assert expected == highlight_doc(basic_document, basic_document + " baz")


def test_highlight_doc_no_hit_query(basic_document):
    assert basic_document == highlight_doc(basic_document, "baz")


def test_is_document_or_query_blank(basic_document, basic_query):
    snippet = Snippet("")
    assert snippet._is_full_text_or_query_blank('')
    assert snippet._is_full_text_or_query_blank(basic_query)
    snippet.full_text = basic_document
    assert snippet._is_full_text_or_query_blank('')
    assert not snippet._is_full_text_or_query_blank(basic_query)


def test_highlight_doc_in_order_query_longer_doc(long_document, long_query):
    highlighted_doc = highlight_doc(long_document, long_query)
    expected_highlight = highlight(long_query)
    assert expected_highlight in highlighted_doc


def test_highlight_doc_with_trailing_puctuation(basic_document, basic_query):
    doc = basic_document + ','
    result = "foo " + highlight("bar") + ','
    assert result == highlight_doc(doc, basic_query)


def test_highlight_doc_case_sensitivity(basic_document, basic_query):
    doc = basic_document.upper()
    result = ("foo " + highlight("bar")).upper()
    assert result == highlight_doc(doc, basic_query)