
def test_dot_sparse_scalar():
    a = coo_array([[1, 2], [3, 4], [5, 6]])
    b = 3
    res = a.dot(b)
    exp = np.dot(a.toarray(), b)
    assert_equal(res.toarray(), exp)

