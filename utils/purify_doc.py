
def purify_doc(string):
    '''Remove Sphinx's :param: and :type: lines from the docstring.'''
    return SPHINX_RE.sub('', string).rstrip()

