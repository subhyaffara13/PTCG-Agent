
def _escape_latex_math(s: str) -> str:
    r"""
    All characters in LaTeX math mode are preserved.

    The substrings in LaTeX math mode, which either are surrounded
    by two characters ``$`` or start with the character ``\(`` and end with ``\)``,
    are preserved without escaping. Otherwise regular LaTeX escaping applies.

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
    ps_d = re.compile(r"\$.*?\$").search(s, 0)
    ps_p = re.compile(r"\(.*?\)").search(s, 0)
    mode = []
    if ps_d:
        mode.append(ps_d.span()[0])
    if ps_p:
        mode.append(ps_p.span()[0])
    if len(mode) == 0:
        return _escape_latex(s.replace(r"rt8§=§7wz", r"\$"))
    if s[mode[0]] == r"$":
        return _math_mode_with_dollar(s.replace(r"rt8§=§7wz", r"\$"))
    if s[mode[0] - 1 : mode[0] + 1] == r"\(":
        return _math_mode_with_parentheses(s.replace(r"rt8§=§7wz", r"\$"))
    else:
        return _escape_latex(s.replace(r"rt8§=§7wz", r"\$"))

