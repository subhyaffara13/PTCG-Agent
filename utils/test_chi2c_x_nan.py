
def test_chi2c_x_nan(v):
    assert np.isnan(special.chdtrc(v, np.nan))

