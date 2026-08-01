
def test__safe_first_finite_all_inf():
    arr = np.full(2, np.inf)
    ret = cbook._safe_first_finite(arr)
    assert np.isinf(ret)

