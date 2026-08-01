
def do_insertions(insertions, tokens):
    """
    Helper for lexers which must combine the results of several
    sublexers.

    ``insertions`` is a list of ``(index, itokens)`` pairs.
    Each ``itokens`` iterable should be inserted at position
    ``index`` into the token stream given by the ``tokens``
    argument.

    The result is a combined token stream.

    TODO: clean up the code here.
    """
    insertions = iter(insertions)
    try:
        index, itokens = next(insertions)
    except StopIteration:
        # no insertions
        yield from tokens
        return

    realpos = None
    insleft = True

    # iterate over the token stream where we want to insert
    # the tokens from the insertion list.
    for i, t, v in tokens:
        # first iteration. store the position of first item
        if realpos is None:
            realpos = i
        oldi = 0
        while insleft and i + len(v) >= index:
            tmpval = v[oldi:index - i]
            if tmpval:
                yield realpos, t, tmpval
                realpos += len(tmpval)
            for it_index, it_token, it_value in itokens:
                yield realpos, it_token, it_value
                realpos += len(it_value)
            oldi = index - i
            try:
                index, itokens = next(insertions)
            except StopIteration:
                insleft = False
                break  # not strictly necessary
        if oldi < len(v):
            yield realpos, t, v[oldi:]
            realpos += len(v) - oldi

    # leftover tokens
    while insleft:
        # no normal tokens, set realpos to zero
        realpos = realpos or 0
        for p, t, v in itokens:
            yield realpos, t, v
            realpos += len(v)
        try:
            index, itokens = next(insertions)
        except StopIteration:
            insleft = False
            break  # not strictly necessary


def do_insertions(insertions, tokens):
    """
    Helper for lexers which must combine the results of several
    sublexers.

    ``insertions`` is a list of ``(index, itokens)`` pairs.
    Each ``itokens`` iterable should be inserted at position
    ``index`` into the token stream given by the ``tokens``
    argument.

    The result is a combined token stream.

    TODO: clean up the code here.
    """
    insertions = iter(insertions)
    try:
        index, itokens = next(insertions)
    except StopIteration:
        # no insertions
        yield from tokens
        return

    realpos = None
    insleft = True

    # iterate over the token stream where we want to insert
    # the tokens from the insertion list.
    for i, t, v in tokens:
        # first iteration. store the position of first item
        if realpos is None:
            realpos = i
        oldi = 0
        while insleft and i + len(v) >= index:
            tmpval = v[oldi:index - i]
            if tmpval:
                yield realpos, t, tmpval
                realpos += len(tmpval)
            for it_index, it_token, it_value in itokens:
                yield realpos, it_token, it_value
                realpos += len(it_value)
            oldi = index - i
            try:
                index, itokens = next(insertions)
            except StopIteration:
                insleft = False
                break  # not strictly necessary
        if oldi < len(v):
            yield realpos, t, v[oldi:]
            realpos += len(v) - oldi

    # leftover tokens
    while insleft:
        # no normal tokens, set realpos to zero
        realpos = realpos or 0
        for p, t, v in itokens:
            yield realpos, t, v
            realpos += len(v)
        try:
            index, itokens = next(insertions)
        except StopIteration:
            insleft = False
            break  # not strictly necessary

