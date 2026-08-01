
def mutate_string(text: str) -> str:
    """Replace contents with 'xxx' to prevent syntax matching.

    >>> mutate_string('"abc"')
    '"xxx"'
    >>> mutate_string("'''abc'''")
    "'''xxx'''"
    >>> mutate_string("r'abc'")
    "r'xxx'"
    """
    # NOTE(sigmavirus24): If there are string modifiers (e.g., b, u, r)
    # use the last "character" to determine if we're using single or double
    # quotes and then find the first instance of it
    start = text.index(text[-1]) + 1
    end = len(text) - 1
    # Check for triple-quoted strings
    if text[-3:] in ('"""', "'''"):
        start += 2
        end -= 2
    return text[:start] + "x" * (end - start) + text[end:]

