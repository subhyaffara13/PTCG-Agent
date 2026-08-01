
def normalize_newlines(text):
    r"""
    Replace alternate newlines with the canonical newline.

    >>> normalize_newlines('Lorem Ipsum\u2029')
    'Lorem Ipsum\n'
    >>> normalize_newlines('Lorem Ipsum\r\n')
    'Lorem Ipsum\n'
    >>> normalize_newlines('Lorem Ipsum\x85')
    'Lorem Ipsum\n'
    """
    newlines = ['\r\n', '\r', '\n', '\u0085', '\u2028', '\u2029']
    pattern = '|'.join(newlines)
    return re.sub(pattern, '\n', text)

