
def test_dot_1d_1d(): # 1-D inner product
    a = coo_array([1,2,3])
    b = coo_array([4,5,6])
    exp = np.dot(a.toarray(), b.toarray())
    res = a.dot(b)
    assert_equal(res, exp)
    res = a.dot(b.toarray())
    assert_equal(res, exp)

