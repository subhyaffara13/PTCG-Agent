
def _parse_latex_table_styles(table_styles: CSSStyles, selector: str) -> str | None:
    """
    Return the first 'props' 'value' from ``tables_styles`` identified by ``selector``.

    Examples
    --------
    >>> table_styles = [
    ...     {"selector": "foo", "props": [("attr", "value")]},
    ...     {"selector": "bar", "props": [("attr", "overwritten")]},
    ...     {"selector": "bar", "props": [("a1", "baz"), ("a2", "ignore")]},
    ... ]
    >>> _parse_latex_table_styles(table_styles, selector="bar")
    'baz'

    Notes
    -----
    The replacement of "§" with ":" is to avoid the CSS problem where ":" has structural
    significance and cannot be used in LaTeX labels, but is often required by them.
    """
    for style in table_styles[::-1]:  # in reverse for most recently applied style
        if style["selector"] == selector:
            return str(style["props"][0][1]).replace("§", ":")
    return None

