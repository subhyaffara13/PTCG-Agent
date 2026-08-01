
def test_sparse_signature(doc):
    pytest.importorskip("scipy")
    assert (
        doc(m.sparse_copy_r)
        == """
        sparse_copy_r(arg0: scipy.sparse.csr_matrix[numpy.float32]) -> scipy.sparse.csr_matrix[numpy.float32]
    """
    )
    assert (
        doc(m.sparse_copy_c)
        == """
        sparse_copy_c(arg0: scipy.sparse.csc_matrix[numpy.float32]) -> scipy.sparse.csc_matrix[numpy.float32]
    """
    )

