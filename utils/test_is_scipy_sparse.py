
def test_is_scipy_sparse():
    sp_sparse = pytest.importorskip("scipy.sparse")

    assert com.is_scipy_sparse(sp_sparse.bsr_matrix([1, 2, 3]))

    assert not com.is_scipy_sparse(SparseArray([1, 2, 3]))


def test_is_scipy_sparse(spmatrix):
    sparse = pytest.importorskip("scipy.sparse")

    klass = getattr(sparse, spmatrix + "_matrix")
    assert is_scipy_sparse(klass([[0, 1]]))
    assert not is_scipy_sparse(np.array([1]))

