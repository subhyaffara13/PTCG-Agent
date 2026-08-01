
def test_good_bounds():
    lp = _LPProblem(c=[1, 2])

    lp_cleaned = _clean_inputs(lp)  # lp.bounds is None by default
    assert_equal(lp_cleaned.bounds, [(0, np.inf)] * 2)

    lp_cleaned = _clean_inputs(lp._replace(bounds=[]))
    assert_equal(lp_cleaned.bounds, [(0, np.inf)] * 2)

    lp_cleaned = _clean_inputs(lp._replace(bounds=[[]]))
    assert_equal(lp_cleaned.bounds, [(0, np.inf)] * 2)

    lp_cleaned = _clean_inputs(lp._replace(bounds=(1, 2)))
    assert_equal(lp_cleaned.bounds, [(1, 2)] * 2)

    lp_cleaned = _clean_inputs(lp._replace(bounds=[(1, 2)]))
    assert_equal(lp_cleaned.bounds, [(1, 2)] * 2)

    lp_cleaned = _clean_inputs(lp._replace(bounds=[(1, None)]))
    assert_equal(lp_cleaned.bounds, [(1, np.inf)] * 2)

    lp_cleaned = _clean_inputs(lp._replace(bounds=[(None, 1)]))
    assert_equal(lp_cleaned.bounds, [(-np.inf, 1)] * 2)

    lp_cleaned = _clean_inputs(lp._replace(bounds=[(None, None), (-np.inf, None)]))
    assert_equal(lp_cleaned.bounds, [(-np.inf, np.inf)] * 2)

    lp = _LPProblem(c=[1, 2, 3, 4])

    lp_cleaned = _clean_inputs(lp)  # lp.bounds is None by default
    assert_equal(lp_cleaned.bounds, [(0, np.inf)] * 4)

    lp_cleaned = _clean_inputs(lp._replace(bounds=(1, 2)))
    assert_equal(lp_cleaned.bounds, [(1, 2)] * 4)

    lp_cleaned = _clean_inputs(lp._replace(bounds=[(1, 2)]))
    assert_equal(lp_cleaned.bounds, [(1, 2)] * 4)

    lp_cleaned = _clean_inputs(lp._replace(bounds=[(1, None)]))
    assert_equal(lp_cleaned.bounds, [(1, np.inf)] * 4)

    lp_cleaned = _clean_inputs(lp._replace(bounds=[(None, 1)]))
    assert_equal(lp_cleaned.bounds, [(-np.inf, 1)] * 4)

    lp_cleaned = _clean_inputs(lp._replace(bounds=[(None, None),
                                                   (-np.inf, None),
                                                   (None, np.inf),
                                                   (-np.inf, np.inf)]))
    assert_equal(lp_cleaned.bounds, [(-np.inf, np.inf)] * 4)

