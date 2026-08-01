
def _logical(tokens):
    '''Find how many logical lines are there in the current line.

    Normally 1 line of code is equivalent to 1 logical line of code,
    but there are cases when this is not true. For example::

        if cond: return 0

    this line actually corresponds to 2 logical lines, since it can be
    translated into::

        if cond:
            return 0

    Examples::

        if cond:  -> 1

        if cond: return 0  -> 2

        try: 1/0  -> 2

        try:  -> 1

        if cond:  # Only a comment  -> 1

        if cond: return 0  # Only a comment  -> 2
    '''

    def aux(sub_tokens):
        '''The actual function which does the job.'''
        # Get the tokens and, in the meantime, remove comments
        processed = list(_fewer_tokens(sub_tokens, [COMMENT, NL, NEWLINE]))
        try:
            # Verify whether a colon is present among the tokens and that
            # it is the last token.
            token_pos = _find(processed, OP, ':')
            # We subtract 2 from the total because the last token is always
            # ENDMARKER. There are two cases: if the colon is at the end, it
            # means that there is only one logical line; if it isn't then there
            # are two.
            return 2 - (token_pos == len(processed) - 2)
        except ValueError:
            # The colon is not present
            # If the line is only composed by comments, newlines and endmarker
            # then it does not count as a logical line.
            # Otherwise it count as 1.
            if not list(_fewer_tokens(processed, [NL, NEWLINE, EM])):
                return 0
            return 1

    return sum(aux(sub) for sub in _split_tokens(tokens, OP, ';'))

