
def test_pct_max_many_rows():
    # GH 18271
    s = Series(np.arange(2**24 + 1))
    result = s.rank(pct=True).max()
    assert result == 1

