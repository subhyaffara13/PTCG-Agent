
def test_inconsistent_dimensions():
    m = 2
    n = 4
    c = [1, 2, 3, 4]

    rng = np.random.default_rng(122390)
    Agood = rng.random((m, n))
    Abad = rng.random((m, n + 1))
    bgood = rng.random(m)
    bbad = rng.random(m + 1)
    boundsbad = [(0, 1)] * (n + 1)
    assert_raises(ValueError, _clean_inputs, _LPProblem(c=c, A_ub=Abad, b_ub=bgood))
    assert_raises(ValueError, _clean_inputs, _LPProblem(c=c, A_ub=Agood, b_ub=bbad))
    assert_raises(ValueError, _clean_inputs, _LPProblem(c=c, A_eq=Abad, b_eq=bgood))
    assert_raises(ValueError, _clean_inputs, _LPProblem(c=c, A_eq=Agood, b_eq=bbad))
    assert_raises(ValueError, _clean_inputs, _LPProblem(c=c, bounds=boundsbad))
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", "Creating an ndarray from ragged", VisibleDeprecationWarning)
        assert_raises(ValueError, _clean_inputs,
                      _LPProblem(c=c, bounds=[[1, 2], [2, 3], [3, 4], [4, 5, 6]]))

