HIGHLIGHT = '[[HIGHLIGHT]]'
END_HIGHLIGHT = '[[ENDHIGHLIGHT]]'


def highlight_doc(document, query):
    if is_document_or_query_blank(document, query):
        return document

    query_terms = query.split(' ')

    document_terms = document.split(' ')

    result_terms = []
    to_highlight = []
    for term in document_terms:
        if term in query_terms:
            to_highlight.append(term)
        else:
            if len(to_highlight) > 0:
                result_terms.append(highlight(' '.join(to_highlight)))
                to_highlight = []
            result_terms.append(term)

    if len(to_highlight) > 0:
        result_terms.append(highlight(' '.join(to_highlight)))

    return ' '.join(result_terms)


def is_document_or_query_blank(document, query):
    if document is '' or query is '':
        return True
    else:
        return False


def highlight(term):
    return HIGHLIGHT + term + END_HIGHLIGHT
