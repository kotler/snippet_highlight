HIGHLIGHT = "[[HIGHLIGHT]]"
END_HIGHLIGHT = "[[ENDHIGHLIGHT]]"


def highlight_doc(document, query):
    if arguments_are_empty(document, query):
        return document


def arguments_are_empty(document, query):
    if document is '' or query is '':
        return True
    else:
        return False
