
def build_token_groups_for_with_subexpression(tokens):
    """
    Yield tuples of Token given a ``tokens`` sequence of Token such that:
     - all "XXX WITH YYY" sequences of 3 tokens are grouped in a three-tuple
     - single tokens are just wrapped in a tuple for consistency.
    """

    # if n-1 is sym, n is with and n+1 is sym: yield this as a group for a with
    # exp otherwise: yield each single token as a group

    tokens = list(tokens)

    # check three contiguous tokens that may form "lic WITh exception" sequence
    triple_len = 3

    # shortcut if there are no grouping possible
    if len(tokens) < triple_len:
        for tok in tokens:
            yield (tok,)
        return

    # accumulate three contiguous tokens
    triple = deque()
    triple_popleft = triple.popleft
    triple_clear = triple.clear
    tripple_append = triple.append

    for tok in tokens:
        if len(triple) == triple_len:
            if is_with_subexpression(triple):
                yield tuple(triple)
                triple_clear()
            else:
                prev_tok = triple_popleft()
                yield (prev_tok,)
        tripple_append(tok)

    # end remainders
    if triple:
        if len(triple) == triple_len and is_with_subexpression(triple):
            yield tuple(triple)
        else:
            for tok in triple:
                yield (tok,)

