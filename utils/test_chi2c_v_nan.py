
def test_chi2c_v_nan(x):
    assert np.isnan(special.chdtrc(np.nan, x))

