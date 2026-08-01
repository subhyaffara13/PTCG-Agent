
def build_symbols_from_unknown_tokens(tokens):
    """
    Yield Token given a ``token`` sequence of Token replacing unmatched
    contiguous tokens by a single token with a LicenseSymbol.
    """
    tokens = list(tokens)

    unmatched = deque()

    def build_token_with_symbol():
        """
        Build and return a new Token from accumulated unmatched tokens or None.
        """
        if not unmatched:
            return
        # strip trailing spaces
        trailing_spaces = []
        while unmatched and not unmatched[-1].string.strip():
            trailing_spaces.append(unmatched.pop())

        if unmatched:
            string = " ".join(t.string for t in unmatched if t.string.strip())
            start = unmatched[0].start
            end = unmatched[-1].end
            toksym = LicenseSymbol(string)
            unmatched.clear()
            yield Token(start, end, string, toksym)

        for ts in trailing_spaces:
            yield ts

    for tok in tokens:
        if tok.value:
            for symtok in build_token_with_symbol():
                yield symtok
            yield tok
        else:
            if not unmatched and not tok.string.strip():
                # skip leading spaces
                yield tok
            else:
                unmatched.append(tok)

    # end remainders
    for symtok in build_token_with_symbol():
        yield symtok

