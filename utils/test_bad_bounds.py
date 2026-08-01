
def test_bad_bounds():
    lp = _LPProblem(c=[1, 2])

    assert_raises(ValueError, _clean_inputs, lp._replace(bounds=(1, 2, 2)))
    assert_raises(ValueError, _clean_inputs, lp._replace(bounds=[(1, 2, 2)]))
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", "Creating an ndarray from ragged", VisibleDeprecationWarning)
        assert_raises(ValueError, _clean_inputs,
                      lp._replace(bounds=[(1, 2), (1, 2, 2)]))
    assert_raises(ValueError, _clean_inputs,
                  lp._replace(bounds=[(1, 2), (1, 2), (1, 2)]))

    lp = _LPProblem(c=[1, 2, 3, 4])

    assert_raises(ValueError, _clean_inputs,
                  lp._replace(bounds=[(1, 2, 3, 4), (1, 2, 3, 4)]))

