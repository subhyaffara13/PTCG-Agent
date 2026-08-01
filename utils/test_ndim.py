
def test_ndim(xp):
    X = xp.asarray([[1]])
    A = interface.aslinearoperator(X)
    assert A.ndim == 2

