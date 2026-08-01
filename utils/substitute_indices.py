
def substitute_indices(t, *index_tuples):
    if not isinstance(t, TensExpr):
        return t
    return t.substitute_indices(*index_tuples)

