import string


def highlight_doc(document, query):
    snippet = Snippet(document, query)
    return snippet.highlighted()


class Snippet(object):
    LENGTH = 256
    HIGHLIGHT = '[[HIGHLIGHT]]'
    END_HIGHLIGHT = '[[ENDHIGHLIGHT]]'

    def __init__(self, full_text, query):
        self.full_text = full_text
        self.query = query
        self.snippet = self._find_most_relevant_snippet()

    def _find_most_relevant_snippet(self):
        """
        1.  Split document in sentences
        2.  Rank each sentence (count of query terms, count of adjacent terms,
            exact query matches)
        3.  Start snippet preferably at the beginning of a sentence. If a
            sentence is longer than window_size make sure snippet contains
            a query term.
        """
        if self._is_full_text_or_query_blank():
            return self.full_text[:self.LENGTH]
        else:
            return self.full_text[:self.LENGTH]

    def _is_full_text_or_query_blank(self):
        if self.full_text is '' or self.query is '':
            return True
        else:
            return False

    def highlighted(self):
        if not self.query:
            return self.snippet

        query_terms = []
        for term in self.query.split(' '):
            query_terms.append(self._prep_term(term))

        snippet_terms = self.snippet.split(' ')

        result_terms = []
        to_highlight = []
        for term in snippet_terms:
            if self._prep_term(term) in query_terms:
                to_highlight.append(term)
            else:
                if len(to_highlight) > 0:
                    result_terms.append(self._highlight(' '.join(
                        to_highlight)))
                    to_highlight = []
                result_terms.append(term)

        if len(to_highlight) > 0:
            result_terms.append(self._highlight(' '.join(to_highlight)))

        return ' '.join(result_terms)

    def _highlight(self, term):
        return (self.HIGHLIGHT + without_trailing_punctuation(term) +
                self.END_HIGHLIGHT + trailing_punctuation(term))

    def _prep_term(self, term):
        return without_trailing_punctuation(term).lower()


class Ranked_Sentence(object):
    QUERY_TERMS_WEIGHT = 0.25
    ADJACENT_QUERY_TERMS_WEIGHT = 0.25
    EXACT_MATCH_WEIGHT = 0.5

    def __init__(self, text, query):
        self.text = text
        self.rank = self.rank(query)

    def rank(self):
        rank = (self.count_of_query_terms() * self.QUERY_TERMS_WEIGHT +
                self.count_of_adjacent_query_terms *
                self.ADJACENT_QUERY_TERMS_WEIGHT +
                self.count_of_exact_matches() * self.EXACT_MATCH_WEIGHT)
        return rank

    def count_of_query_terms(self):
        return 0

    def count_of_adjacent_query_terms(self):
        return 0

    def count_of_exact_matches(self):
        return 0


def without_trailing_punctuation(text):
    if len(text) < 1:
        return text
    if text[len(text) - 1] in string.punctuation:
        text = without_trailing_punctuation(text[:-1])
    return text


def trailing_punctuation(text):
    result = ""
    if len(text) < 1:
        return result
    position = len(text) - 1
    while text[position] in string.punctuation:
        result = text[position] + result
        position -= 1
    return result
