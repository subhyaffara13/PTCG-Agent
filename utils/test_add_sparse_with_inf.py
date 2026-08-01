
def test_add_sparse_with_inf():
    # addition of sparse arrays with an inf element
    den_a = np.array([[[0], [np.inf]], [[-3], [0]]])
    den_b = np.array([[[0], [1]], [[2], [3]]])
    dense_sum = den_a + den_b
    sparse_sum = coo_array(den_a) + coo_array(den_b)
    assert_equal(dense_sum, sparse_sum.toarray())

