
def test_too_few_dimensions():
    rng = np.random.default_rng(1234)
    bad = rng.random((4, 4)).ravel()
    cb = rng.random(4)
    assert_raises(ValueError, _clean_inputs, _LPProblem(c=cb, A_ub=bad, b_ub=cb))
    assert_raises(ValueError, _clean_inputs, _LPProblem(c=cb, A_eq=bad, b_eq=cb))

