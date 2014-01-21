import unittest
from nose.tools import *  # PEP8 asserts
from snippet_highlight import snippet_highlight


class SnippetHighlightTest(unittest.TestCase):

    def setUp(self):
        self.basic_document = "foo bar"
        self.basic_query = "bar"
        self.basic_result = ("foo " + snippet_highlight.HIGHLIGHT + "bar" +
                             snippet_highlight.END_HIGHLIGHT)

    def tearDown(self):
        pass

    def test_basic_highlight_doc(self):
        assert_equal('', snippet_highlight.highlight_doc('', ''))
        assert_equal(self.basic_document,
                     snippet_highlight.highlight_doc(self.basic_document, ''))
        assert_equal('',
                     snippet_highlight.highlight_doc('', self.basic_query))
        assert_equal(self.basic_result,
                     snippet_highlight.highlight_doc(self.basic_document,
                                                     self.basic_query))

    def test_arguments_are_empty(self):
        assert_true(snippet_highlight.arguments_are_empty('', ''))
        assert_true(snippet_highlight.arguments_are_empty('',
                                                          self.basic_query))
        assert_true(snippet_highlight.arguments_are_empty(self.basic_document,
                                                          ''))
        assert_false(snippet_highlight.arguments_are_empty(self.basic_document,
                                                           self.basic_query))


if __name__ == '__main__':
    unittest.main()
