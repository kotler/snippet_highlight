import unittest
from nose.tools import *  # PEP8 asserts
from snippet_highlight import snippet_highlight


class SnippetHighlightTest(unittest.TestCase):

    def setUp(self):
        self.basic_document = "foo bar"
        self.basic_query = "bar"
        self.highlighted_foo = self.highlight("foo")
        self.highlighted_bar = self.highlight("bar")
        self.basic_result = "foo " + self.highlight("bar")
        self.multi_word_result = self.highlight(self.basic_document)
        self.test_file = open("tests/test_document.txt")
        self.long_document = self.test_file.read()
        self.long_query = "George Lucas"
        self.highlighted_long_query = (
            self.highlight(self.long_query))

    def tearDown(self):
        self.test_file.close()

    def highlighted_in_order_query(self, query):
        query_words = query.split(' ')
        result = ''
        for word in query_words:
            result += self.highlight_word(query)
        return result

    def highlight(self, text):
        return (snippet_highlight.HIGHLIGHT + text +
                snippet_highlight.END_HIGHLIGHT)

    def test_highlight_doc_blank_doc_and_query(self):
        assert_equal('', snippet_highlight.highlight_doc('', ''))

    def test_highlight_doc_blank_query(self):
        assert_equal(self.basic_document,
                     snippet_highlight.highlight_doc(self.basic_document, ''))

    def test_highlight_doc_blank_doc(self):
        assert_equal('',
                     snippet_highlight.highlight_doc('', self.basic_query))

    def test_highlight_doc(self):
        assert_equal(self.basic_result,
                     snippet_highlight.highlight_doc(self.basic_document,
                                                     self.basic_query))

    def test_highlight_doc_multiple_words(self):
        assert_equal(self.multi_word_result, snippet_highlight.highlight_doc(
            self.basic_document, self.basic_document))

    def test_highlight_doc_longer_query_than_doc(self):
        assert_equal(self.multi_word_result, snippet_highlight.highlight_doc(
            self.basic_document, self.basic_document + " baz"))

    def test_highlight_doc_no_hit_query(self):
        assert_equal(self.basic_document, snippet_highlight.highlight_doc(
            self.basic_document, "baz"))

    def test_is_document_or_query_blank(self):
        assert_true(snippet_highlight.is_document_or_query_blank('', ''))
        assert_true(snippet_highlight.is_document_or_query_blank('',
                    self.basic_query))
        assert_true(snippet_highlight.is_document_or_query_blank(
            self.basic_document, ''))
        assert_false(snippet_highlight.is_document_or_query_blank(
            self.basic_document, self.basic_query))

    def test_highlight_doc_in_order_query_longer_doc(self):
        assert_is_not(-1,
                      snippet_highlight.highlight_doc(self.long_document,
                                                      self.long_query).find(
                          self.highlighted_long_query))

    def test_highlight_doc_with_trailing_puctuation(self):
        doc = self.basic_document + ','
        result = self.basic_result + ','
        assert_equal(snippet_highlight.highlight_doc(doc, self.basic_query),
                     result)

if __name__ == '__main__':
    unittest.main()
