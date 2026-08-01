
def test_dot_nd(a_shape, b_shape):
    rng = np.random.default_rng(23409823)

    arr_a = random_array(a_shape, density=0.6, random_state=rng, dtype=int)
    arr_b = random_array(b_shape, density=0.6, random_state=rng, dtype=int)

    exp = np.dot(arr_a.toarray(), arr_b.toarray())
    # sparse-dense
    res = arr_a.dot(arr_b.toarray())
    assert_equal(res, exp)
    res = arr_a.dot(list(arr_b.toarray()))
    assert_equal(res, exp)
    # sparse-sparse
    res = arr_a.dot(arr_b)
    assert_equal(res.toarray(), exp)

