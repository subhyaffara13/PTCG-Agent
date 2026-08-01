
def test_pow_abs_round():
    rng = np.random.default_rng(23409823)
    a = random_array((3,6,5,2,4), density=0.6, random_state=rng, dtype=int)
    assert_allclose((a**3).toarray(), np.power(a.toarray(), 3))
    assert_allclose((a**7).toarray(), np.power(a.toarray(), 7))
    assert_allclose(round(a).toarray(), np.round(a.toarray()))
    assert_allclose(abs(a).toarray(), np.abs(a.toarray()))

