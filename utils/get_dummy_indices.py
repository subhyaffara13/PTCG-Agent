
def get_dummy_indices(t):
    if not isinstance(t, TensExpr):
        return ()
    inds = t.get_indices()
    free = t.get_free_indices()
    return [i for i in inds if i not in free]

