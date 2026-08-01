
def test_argmax_argmin(shape, axis):
    rng = np.random.default_rng(23409823)
    a = random_array(shape, density=0.6, random_state=rng, dtype=int)

    res = a.argmax(axis=axis)
    exp = np.argmax(a.toarray(), axis=axis)
    assert_equal(res, exp)

    res = a.argmin(axis=axis)
    exp = np.argmin(a.toarray(), axis=axis)
    assert_equal(res, exp)

