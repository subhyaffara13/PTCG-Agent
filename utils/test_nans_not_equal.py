
def test_nans_not_equal():
    # GH 54770
    a = SparseDtype(float, 0)
    b = SparseDtype(float, pd.NA)
    assert a != b
    assert b != a

