
def test_where_inplace():
    s = Series(np.random.default_rng(2).standard_normal(5))
    cond = s > 0

    rs = s.copy()

    result = rs.where(cond, inplace=True)
    assert result is rs
    tm.assert_series_equal(rs.dropna(), s[cond])
    tm.assert_series_equal(rs, s.where(cond))

    rs = s.copy()
    result = rs.where(cond, -s, inplace=True)
    assert result is rs
    tm.assert_series_equal(rs, s.where(cond, -s))

