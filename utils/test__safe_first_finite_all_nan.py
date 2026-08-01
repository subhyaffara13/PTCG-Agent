
def test__safe_first_finite_all_nan():
    arr = np.full(2, np.nan)
    ret = cbook._safe_first_finite(arr)
    assert np.isnan(ret)

