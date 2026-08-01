
def test_chi2_v_nan(x):
    assert np.isnan(special.chdtr(np.nan, x))

