
def test_multiply(a_shape, b_shape):
    rng = np.random.default_rng(23409823)
    a = random_array(a_shape, density=0.6, random_state=rng, dtype=int)
    b = random_array(b_shape, density=0.6, random_state=rng, dtype=int)
    res = a * b
    exp = np.multiply(a.toarray(), b.toarray())
    assert_equal(res.toarray(), exp)

