
def test_nans_equal():
    a = SparseDtype(float, float("nan"))
    b = SparseDtype(float, np.nan)
    assert a == b
    assert b == a

