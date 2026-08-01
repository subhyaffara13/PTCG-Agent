
def test_matrix_zeros_scipy():
    if not np:
        skip("numpy not installed.")
    if not scipy:
        skip("scipy not installed.")

    sci = matrix_zeros(4, 4, format='scipy.sparse')
    assert isinstance(sci, scipy_sparse_matrix)

