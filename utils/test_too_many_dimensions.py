
def test_too_many_dimensions():
    cb = [1, 2, 3, 4]
    rng = np.random.default_rng(1234)
    A = rng.random((4, 4))
    bad2D = [[1, 2], [3, 4]]
    bad3D = rng.random((4, 4, 4))
    assert_raises(ValueError, _clean_inputs, _LPProblem(c=bad2D, A_ub=A, b_ub=cb))
    assert_raises(ValueError, _clean_inputs, _LPProblem(c=cb, A_ub=bad3D, b_ub=cb))
    assert_raises(ValueError, _clean_inputs, _LPProblem(c=cb, A_ub=A, b_ub=bad2D))
    assert_raises(ValueError, _clean_inputs, _LPProblem(c=cb, A_eq=bad3D, b_eq=cb))
    assert_raises(ValueError, _clean_inputs, _LPProblem(c=cb, A_eq=A, b_eq=bad2D))

