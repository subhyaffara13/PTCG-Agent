
def test_2d_matmul_multivector():
    # sparse-sparse matmul
    den = np.array([[0, 1, 2, 3], [3, 2, 1, 0]])
    arr2d = coo_array(den)
    exp = den @ den.T
    res = arr2d @ arr2d.T
    assert_equal(res.toarray(), exp)

    # sparse-dense matmul for self.ndim = 2
    den = np.array([[0, 4, 3, 0, 5], [1, 0, 7, 3, 4]])
    arr2d = coo_array(den)
    exp = den @ den.T
    res = arr2d @ den.T
    assert_equal(res, exp)

    # sparse-dense matmul for self.ndim = 1
    den_a = np.array([[0, 4, 3, 0, 5], [1, 0, 7, 3, 4]])
    den_b = np.array([0, 1, 6, 0, 4])
    arr1d = coo_array(den_b)
    exp = den_b @ den_a.T
    res = arr1d @ den_a.T
    assert_equal(res, exp)

    # sparse-dense matmul for self.ndim = 1 and other.ndim = 2
    den_a = np.array([1, 0, 2])
    den_b = np.array([[3], [4], [0]])
    exp = den_a @ den_b
    res = coo_array(den_a) @ den_b
    assert_equal(res, exp)
    res = coo_array(den_a) @ list(den_b)
    assert_equal(res, exp)

