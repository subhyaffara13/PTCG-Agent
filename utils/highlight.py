
def highlight(code, lexer, formatter, outfile=None):
    """
    This is the most high-level highlighting function. It combines `lex` and
    `format` in one function.
    """
    return format(lex(code, lexer), formatter, outfile)


def highlight(code, lexer, formatter, outfile=None):
    """
    This is the most high-level highlighting function. It combines `lex` and
    `format` in one function.
    """
    return format(lex(code, lexer), formatter, outfile)

