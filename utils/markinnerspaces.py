
def markinnerspaces(line):
    """
    The function replace all spaces in the input variable line which are
    surrounded with quotation marks, with the triplet "@_@".

    For instance, for the input "a 'b c'" the function returns "a 'b@_@c'"

    Parameters
    ----------
    line : str

    Returns
    -------
    str

    """
    fragment = ''
    inside = False
    current_quote = None
    escaped = ''
    for c in line:
        if escaped == '\\' and c in ['\\', '\'', '"']:
            fragment += c
            escaped = c
            continue
        if not inside and c in ['\'', '"']:
            current_quote = c
        if c == current_quote:
            inside = not inside
        elif c == ' ' and inside:
            fragment += '@_@'
            continue
        fragment += c
        escaped = c  # reset to non-backslash
    return fragment

