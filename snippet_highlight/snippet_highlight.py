import string
import re


def highlight_doc(document, query):
    snippet = Snippet(document)
    snippet.set_snippet_relevant_to(query)
    return snippet.highlight(query)


class Snippet(object):
    LENGTH = 256
    HIGHLIGHT = '[[HIGHLIGHT]]'
    END_HIGHLIGHT = '[[ENDHIGHLIGHT]]'

    def __init__(self, full_text):
        self.full_text = full_text
        self.snippet = self._find_most_relevant_snippet('')

    def set_snippet_relevant_to(self, query_text):
        self.snippet = self._find_most_relevant_snippet(query_text)
        return self.snippet

    def highlight(self, text):
        if not text:
            return self.snippet

        text_terms = []
        for term in text.split(' '):
            text_terms.append(self._prep_term_for_matching(term))

        snippet_terms = self.snippet.split(' ')
        self.snippet = self._highlight(snippet_terms, text_terms)
        return self.snippet

    def _find_most_relevant_snippet(self, query_text):
        if self._is_full_text_or_query_blank(query_text):
            return self.full_text[:self.LENGTH]

        query_terms = [re.escape(term) for term in query_text.lower().split()]
        if not query_terms:
            return self.full_text[:self.LENGTH]

        # Find all occurrences of all query terms
        pattern = re.compile('|'.join(query_terms), re.IGNORECASE)
        matches = list(pattern.finditer(self.full_text))

        if not matches:
            return self.full_text[:self.LENGTH]

        # Score each match by the density of other matches nearby
        best_match = None
        max_score = -1

        for i, match in enumerate(matches):
            score = 0
            center = match.start()
            for other_match in matches[i:]:
                if other_match.start() >= center + self.LENGTH:
                    break
                score += 1
            
            if score > max_score:
                max_score = score
                best_match = match

        # Create the snippet around the best match
        sentence_center = best_match.start() + len(best_match.group(0)) // 2
        start = max(0, sentence_center - self.LENGTH // 2)
        end = min(len(self.full_text), start + self.LENGTH)

        return self.full_text[start:end]

    def _is_full_text_or_query_blank(self, query_text):
        return not self.full_text or not query_text

    def _highlight(self, text_terms, query_terms):
        result_terms = []
        to_highlight = []
        for term in text_terms:
            if self._prep_term_for_matching(term) in query_terms:
                to_highlight.append(term)
            else:
                result_terms, to_highlight = self._append_and_highlight_terms(
                    result_terms, to_highlight)
                result_terms.append(term)

        result_terms, to_highlight = self._append_and_highlight_terms(
            result_terms, to_highlight)
        return ' '.join(result_terms)

    def _append_and_highlight_terms(self, result_terms, to_highlight):
        if len(to_highlight) > 0:
            result_terms.append(self._highlight_term(' '.join(to_highlight)))
            to_highlight = []
        return result_terms, to_highlight

    def _highlight_term(self, term):
        return (self.HIGHLIGHT + without_trailing_punctuation(term) +
                self.END_HIGHLIGHT + trailing_punctuation(term))

    def _prep_term_for_matching(self, term):
        return without_trailing_punctuation(term).lower()





def without_trailing_punctuation(text):
    while len(text) > 0 and text[-1] in string.punctuation:
        text = text[:-1]
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
