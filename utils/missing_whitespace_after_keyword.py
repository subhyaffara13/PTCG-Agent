
def missing_whitespace_after_keyword(logical_line, tokens):
    r"""Keywords should be followed by whitespace.

    Okay: from foo import (bar, baz)
    E275: from foo import(bar, baz)
    E275: from importable.module import(bar, baz)
    E275: if(foo): bar
    """
    for tok0, tok1 in zip(tokens, tokens[1:]):
        # This must exclude the True/False/None singletons, which can
        # appear e.g. as "if x is None:", and async/await, which were
        # valid identifier names in old Python versions.
        if (tok0.end == tok1.start and
                tok0.type == tokenize.NAME and
                keyword.iskeyword(tok0.string) and
                tok0.string not in SINGLETONS and
                not (tok0.string == 'except' and tok1.string == '*') and
                not (tok0.string == 'yield' and tok1.string == ')') and
                tok1.string not in ':\n'):
            yield tok0.end, "E275 missing whitespace after keyword"

