
def test_getrow_getcol(A):
    assert isinstance(A._getcol(0), scipy.sparse.sparray)
    assert isinstance(A._getrow(0), scipy.sparse.sparray)

