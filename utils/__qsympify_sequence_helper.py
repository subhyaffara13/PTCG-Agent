
def __qsympify_sequence_helper(seq):
    """
       Helper function for _qsympify_sequence
       This function does the actual work.
    """
    #base case. If not a list, do Sympification
    if not is_sequence(seq):
        if isinstance(seq, Matrix):
            return seq
        elif isinstance(seq, str):
            return Symbol(seq)
        else:
            return sympify(seq)

    # base condition, when seq is QExpr and also
    # is iterable.
    if isinstance(seq, QExpr):
        return seq

    #if list, recurse on each item in the list
    result = [__qsympify_sequence_helper(item) for item in seq]

    return Tuple(*result)

