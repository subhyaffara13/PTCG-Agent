
def _check_csr_rowslice(i, sl, X, Xcsr):
    np_slice = X[i, sl]
    csr_slice = Xcsr[i, sl]
    assert_array_almost_equal(np_slice, csr_slice.toarray()[0])
    assert_(type(csr_slice) is csr_matrix)

