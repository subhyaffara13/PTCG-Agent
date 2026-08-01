
def lex(code, lexer):
    """
    Lex `code` with the `lexer` (must be a `Lexer` instance)
    and return an iterable of tokens. Currently, this only calls
    `lexer.get_tokens()`.
    """
    try:
        return lexer.get_tokens(code)
    except TypeError:
        # Heuristic to catch a common mistake.
        from pygments.lexer import RegexLexer
        if isinstance(lexer, type) and issubclass(lexer, RegexLexer):
            raise TypeError('lex() argument must be a lexer instance, '
                            'not a class')
        raise


def lex(code, lexer):
    """
    Lex `code` with the `lexer` (must be a `Lexer` instance)
    and return an iterable of tokens. Currently, this only calls
    `lexer.get_tokens()`.
    """
    try:
        return lexer.get_tokens(code)
    except TypeError:
        # Heuristic to catch a common mistake.
        from pip._vendor.pygments.lexer import RegexLexer
        if isinstance(lexer, type) and issubclass(lexer, RegexLexer):
            raise TypeError('lex() argument must be a lexer instance, '
                            'not a class')
        raise

