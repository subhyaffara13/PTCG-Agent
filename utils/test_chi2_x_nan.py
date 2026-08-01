
def test_chi2_x_nan(v):
    assert np.isnan(special.chdtr(v, np.nan))

