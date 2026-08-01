
def test_bdtrik_nbdtrik_inf():
    y = np.array(
        [np.nan,-np.inf,-10.0, -1.0, 0.0, .00001, .5, 0.9999, 1.0, 10.0, np.inf])
    y = y[:,None]
    p = np.atleast_2d(
        [np.nan, -np.inf, -10.0, -1.0, 0.0, .00001, .5, 1.0, np.inf])
    assert np.all(np.isnan(sp.bdtrik(y, np.inf, p)))
    assert np.all(np.isnan(sp.nbdtrik(y, np.inf, p)))

