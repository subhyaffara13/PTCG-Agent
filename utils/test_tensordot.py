
def test_tensordot(a_shape, b_shape, axes):
    rng = np.random.default_rng(23409823)

    arr_a = random_array(a_shape, density=0.6, random_state=rng, dtype=int)
    arr_b = random_array(b_shape, density=0.6, random_state=rng, dtype=int)

    exp = np.tensordot(arr_a.toarray(), arr_b.toarray(), axes=axes)

    # sparse-dense
    res = arr_a.tensordot(arr_b.toarray(), axes=axes)
    assert_equal(res, exp)
    res = arr_a.tensordot(list(arr_b.toarray()), axes=axes)
    assert_equal(res, exp)

    # sparse-sparse
    res = arr_a.tensordot(arr_b, axes=axes)
    if type(res) is coo_array:
        assert_equal(res.toarray(), exp)
    else:
        assert_equal(res, exp)


def test_tensordot():
    # np.linalg.tensordot is just an alias for np.tensordot
    x = np.arange(6).reshape((2, 3))

    assert np.linalg.tensordot(x, x) == 55
    assert np.linalg.tensordot(x, x, axes=[(0, 1), (0, 1)]) == 55

