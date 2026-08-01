
def test_stdtr_stdtrit_neg_inf():
    # -inf was treated as +inf and values from the normal were returned
    assert np.all(np.isnan(sp.stdtr(-np.inf, [-np.inf, -1.0, 0.0, 1.0, np.inf])))
    assert np.all(np.isnan(sp.stdtrit(-np.inf, [0.0, 0.25, 0.5, 0.75, 1.0])))

