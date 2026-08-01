
def get_free_indices(t):
    if not isinstance(t, TensExpr):
        return ()
    return t.get_free_indices()

