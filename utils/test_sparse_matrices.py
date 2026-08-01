
def test_sparse_matrices():
    spm = SparseMatrix.diag(1, 0)
    assert unchanged(TensorProduct, spm, spm)


def test_sparse_matrices():
    # Test that using lil,csr and csc sparse matrix do not cause error
    G_dense = np.array([[0, 3, 0, 0, 0],
                        [0, 0, -1, 0, 0],
                        [0, 0, 0, 2, 0],
                        [0, 0, 0, 0, 4],
                        [0, 0, 0, 0, 0]], dtype=float)
    SP = shortest_path(G_dense)
    G_csr = scipy.sparse.csr_array(G_dense)
    G_csc = scipy.sparse.csc_array(G_dense)
    G_lil = scipy.sparse.lil_array(G_dense)
    assert_array_almost_equal(SP, shortest_path(G_csr))
    assert_array_almost_equal(SP, shortest_path(G_csc))
    assert_array_almost_equal(SP, shortest_path(G_lil))

