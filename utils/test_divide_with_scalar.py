
def test_divide_with_scalar():
    rng = np.random.default_rng(23409823)
    a = random_array((3,5,4), density=0.6, random_state=rng, dtype=int)
    res = a / 7
    exp = a.toarray() / 7
    assert_allclose(res.toarray(), exp)

