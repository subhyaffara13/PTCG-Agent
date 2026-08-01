
def test__clean_inputs1():
    lp = _LPProblem(
        c=[1, 2],
        A_ub=[[1, 1], [2, 2]],
        b_ub=[1, 1],
        A_eq=[[1, 1], [2, 2]],
        b_eq=[1, 1],
        bounds=None
    )

    lp_cleaned = _clean_inputs(lp)

    assert_allclose(lp_cleaned.c, np.array(lp.c))
    assert_allclose(lp_cleaned.A_ub, np.array(lp.A_ub))
    assert_allclose(lp_cleaned.b_ub, np.array(lp.b_ub))
    assert_allclose(lp_cleaned.A_eq, np.array(lp.A_eq))
    assert_allclose(lp_cleaned.b_eq, np.array(lp.b_eq))
    assert_equal(lp_cleaned.bounds, [(0, np.inf)] * 2)

    assert_(lp_cleaned.c.shape == (2,), "")
    assert_(lp_cleaned.A_ub.shape == (2, 2), "")
    assert_(lp_cleaned.b_ub.shape == (2,), "")
    assert_(lp_cleaned.A_eq.shape == (2, 2), "")
    assert_(lp_cleaned.b_eq.shape == (2,), "")

