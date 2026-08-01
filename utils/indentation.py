
def indentation(logical_line, previous_logical, indent_char,
                indent_level, previous_indent_level,
                indent_size):
    r"""Use indent_size (PEP8 says 4) spaces per indentation level.

    For really old code that you don't want to mess up, you can continue
    to use 8-space tabs.

    Okay: a = 1
    Okay: if a == 0:\n    a = 1
    E111:   a = 1
    E114:   # a = 1

    Okay: for item in items:\n    pass
    E112: for item in items:\npass
    E115: for item in items:\n# Hi\n    pass

    Okay: a = 1\nb = 2
    E113: a = 1\n    b = 2
    E116: a = 1\n    # b = 2
    """
    c = 0 if logical_line else 3
    tmpl = "E11%d %s" if logical_line else "E11%d %s (comment)"
    if indent_level % indent_size:
        yield 0, tmpl % (
            1 + c,
            "indentation is not a multiple of " + str(indent_size),
        )
    indent_expect = previous_logical.endswith(':')
    if indent_expect and indent_level <= previous_indent_level:
        yield 0, tmpl % (2 + c, "expected an indented block")
    elif not indent_expect and indent_level > previous_indent_level:
        yield 0, tmpl % (3 + c, "unexpected indentation")

    if indent_expect:
        expected_indent_amount = 8 if indent_char == '\t' else 4
        expected_indent_level = previous_indent_level + expected_indent_amount
        if indent_level > expected_indent_level:
            yield 0, tmpl % (7, 'over-indented')

