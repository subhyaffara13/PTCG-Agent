
def test__clean_inputs3():
    rng = np.random.default_rng(1890908)
    lp = _LPProblem(
        c=[[1, 2]],
        A_ub=rng.random((2, 2)),
        b_ub=[[1], [2]],
        A_eq=rng.random((2, 2)),
        b_eq=[[1], [2]],
        bounds=[(0, 1)]
    )

    lp_cleaned = _clean_inputs(lp)

    assert_allclose(lp_cleaned.c, np.array([1, 2]))
    assert_allclose(lp_cleaned.b_ub, np.array([1, 2]))
    assert_allclose(lp_cleaned.b_eq, np.array([1, 2]))
    assert_equal(lp_cleaned.bounds, [(0, 1)] * 2)

    assert_(lp_cleaned.c.shape == (2,), "")
    assert_(lp_cleaned.b_ub.shape == (2,), "")
    assert_(lp_cleaned.b_eq.shape == (2,), "")

