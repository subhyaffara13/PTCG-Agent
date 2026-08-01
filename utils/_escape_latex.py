
def _escape_latex(s: str) -> str:
    r"""
    Replace the characters ``&``, ``%``, ``$``, ``#``, ``_``, ``{``, ``}``,
    ``~``, ``^``, and ``\`` in the string with LaTeX-safe sequences.

    Use this if you need to display text that might contain such characters in LaTeX.

    Parameters
    ----------
    s : str
        Input to be escaped

    Return
    ------
    str :
        Escaped string
    """
    return (
        s.replace("\\", "ab2§=§8yz")  # rare string for final conversion: avoid \\ clash
        .replace("ab2§=§8yz ", "ab2§=§8yz\\space ")  # since \backslash gobbles spaces
        .replace("&", "\\&")
        .replace("%", "\\%")
        .replace("$", "\\$")
        .replace("#", "\\#")
        .replace("_", "\\_")
        .replace("{", "\\{")
        .replace("}", "\\}")
        .replace("~ ", "~\\space ")  # since \textasciitilde gobbles spaces
        .replace("~", "\\textasciitilde ")
        .replace("^ ", "^\\space ")  # since \textasciicircum gobbles spaces
        .replace("^", "\\textasciicircum ")
        .replace("ab2§=§8yz", "\\textbackslash ")
    )

