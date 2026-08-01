
def _esc_str(s: Any, apply_repr: bool = False) -> str:
    """
    Escapes curly brackets for format strings.
    e.g. "frozenset({0})" becomes "frozenset({{0}})".
    This is used by _name_template for example, because it's
    expected to return a format string, but we may wish to include
    strings that should not be accidentally formatted.
    """
    if apply_repr:
        s = repr(s)
    else:
        s = str(s)
    return s.replace("{", "{{").replace("}", "}}")

