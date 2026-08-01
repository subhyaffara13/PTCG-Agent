
def latex_escape(s: str) -> str:
    """
    Escape a string such that latex interprets it as plaintext.

    We cannot use verbatim easily with mathjax, so escaping is easier.
    Rules from https://tex.stackexchange.com/a/34586/41112.
    """
    s = s.replace('\\', r'\textbackslash')
    for c in '&%$#_{}':
        s = s.replace(c, '\\' + c)
    s = s.replace('~', r'\textasciitilde')
    s = s.replace('^', r'\textasciicircum')
    return s

