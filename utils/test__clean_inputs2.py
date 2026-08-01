
def test__clean_inputs2():
    lp = _LPProblem(
        c=1,
        A_ub=[[1]],
        b_ub=1,
        A_eq=[[1]],
        b_eq=1,
        bounds=(0, 1)
    )

    lp_cleaned = _clean_inputs(lp)

    assert_allclose(lp_cleaned.c, np.array(lp.c))
    assert_allclose(lp_cleaned.A_ub, np.array(lp.A_ub))
    assert_allclose(lp_cleaned.b_ub, np.array(lp.b_ub))
    assert_allclose(lp_cleaned.A_eq, np.array(lp.A_eq))
    assert_allclose(lp_cleaned.b_eq, np.array(lp.b_eq))
    assert_equal(lp_cleaned.bounds, [(0, 1)])

    assert_(lp_cleaned.c.shape == (1,), "")
    assert_(lp_cleaned.A_ub.shape == (1, 1), "")
    assert_(lp_cleaned.b_ub.shape == (1,), "")
    assert_(lp_cleaned.A_eq.shape == (1, 1), "")
    assert_(lp_cleaned.b_eq.shape == (1,), "")

