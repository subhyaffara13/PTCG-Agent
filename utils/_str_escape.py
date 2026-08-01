
def _str_escape(x, escape):
    """if escaping: only use on str, else return input"""
    if isinstance(x, str):
        if escape == "html":
            return escape_html(x)
        elif escape == "latex":
            return _escape_latex(x)
        elif escape == "latex-math":
            return _escape_latex_math(x)
        else:
            raise ValueError(
                f"`escape` only permitted in {{'html', 'latex', 'latex-math'}}, \
got {escape}"
            )
    return x

