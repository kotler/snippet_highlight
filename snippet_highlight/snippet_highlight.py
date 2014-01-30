HIGHLIGHT = '[[HIGHLIGHT]]'
END_HIGHLIGHT = '[[ENDHIGHLIGHT]]'


def highlight_doc(document, query):
    if is_document_or_query_blank(document, query):
        return document

    query_terms = query.split(' ')

    for term in query_terms:
        document = highlight(document, term)
    return document


def is_document_or_query_blank(document, query):
    if document is '' or query is '':
        return True
    else:
        return False


def highlight(text, term):
    highlighted_term = HIGHLIGHT + term + END_HIGHLIGHT
    # FIX_ME string.replace() replaces substrings
    return text.replace(term, highlighted_term)
