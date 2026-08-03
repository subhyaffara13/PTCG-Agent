import re

def _math_mode_with_dollar(s: str) -> str:
    r"""
    All characters in LaTeX math mode are preserved.

    The substrings in LaTeX math mode, which start with
    the character ``$`` and end with ``$``, are preserved
    without escaping. Otherwise regular LaTeX escaping applies.

    Parameters
    ----------
    s : str
        Input to be escaped

    Return
    ------
    str :
        Escaped string
    """
    s = s.replace(r"\$", r"rt8§=§7wz")
    pattern = re.compile(r"\$.*?\$")
    pos = 0
    ps = pattern.search(s, pos)
    res = []
    while ps:
        res.append(_escape_latex(s[pos : ps.span()[0]]))
        res.append(ps.group())
        pos = ps.span()[1]
        ps = pattern.search(s, pos)

    res.append(_escape_latex(s[pos : len(s)]))
    return "".join(res).replace(r"rt8§=§7wz", r"\$")

