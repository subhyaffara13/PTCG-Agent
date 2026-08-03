import re

def _math_mode_with_parentheses(s: str) -> str:
    r"""
    All characters in LaTeX math mode are preserved.

    The substrings in LaTeX math mode, which start with
    the character ``\(`` and end with ``\)``, are preserved
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
    s = s.replace(r"\(", r"LEFT§=§6yzLEFT").replace(r"\)", r"RIGHTab5§=§RIGHT")
    res = []
    for item in re.split(r"LEFT§=§6yz|ab5§=§RIGHT", s):
        if item.startswith("LEFT") and item.endswith("RIGHT"):
            res.append(item.replace("LEFT", r"\(").replace("RIGHT", r"\)"))
        elif "LEFT" in item and "RIGHT" in item:
            res.append(
                _escape_latex(item).replace("LEFT", r"\(").replace("RIGHT", r"\)")
            )
        else:
            res.append(
                _escape_latex(item)
                .replace("LEFT", r"\textbackslash (")
                .replace("RIGHT", r"\textbackslash )")
            )
    return "".join(res)

