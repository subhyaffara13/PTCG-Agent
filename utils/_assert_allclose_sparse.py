
def _assert_allclose_sparse(a, b, **kwargs):
    # helper function that can deal with sparse matrices
    if sparse.issparse(a):
        a = a.toarray()
    if sparse.issparse(b):
        b = b.toarray()
    assert_allclose(a, b, **kwargs)

