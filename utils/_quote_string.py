
def _quote_string(s):
    """Given a string `s`, return a python literal expression that give `s` when it is used in a python source code.

    For example, if `s` is the string `abc`, the return value is `"abc"`.

    We choice double quotes over single quote despite `str(s)` would give `'abc'` instead of `"abc"`.
    """
    has_single_quote = "'" in s
    has_double_quote = '"' in s

    if has_single_quote and has_double_quote:
        # replace any double quote by the raw string r'\"'.
        s = s.replace('"', r"\"")
        return f'"{s}"'
    elif has_single_quote:
        return f'"{s}"'
    elif has_double_quote:
        return f"'{s}'"
    else:
        return f'"{s}"'

