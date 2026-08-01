
def _check_save_and_load(dense_matrix):
    for matrix_class in [csc_matrix, csr_matrix, bsr_matrix, dia_matrix, coo_matrix]:
        matrix = matrix_class(dense_matrix)
        loaded_matrix = _save_and_load(matrix)
        assert_(type(loaded_matrix) is matrix_class)
        assert_(loaded_matrix.shape == dense_matrix.shape)
        assert_(loaded_matrix.dtype == dense_matrix.dtype)
        assert_equal(loaded_matrix.toarray(), dense_matrix)

