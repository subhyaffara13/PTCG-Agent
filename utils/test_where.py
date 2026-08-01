
def test_where():
    X = Geometric('X', Rational(1, 5))
    Y = Poisson('Y', 4)
    assert where(X**2 > 4).set == Range(3, S.Infinity, 1)
    assert where(X**2 >= 4).set == Range(2, S.Infinity, 1)
    assert where(Y**2 < 9).set == Range(0, 3, 1)
    assert where(Y**2 <= 9).set == Range(0, 4, 1)


def test_where():
    X, Y = Die('X'), Die('Y')
    Z = Normal('Z', 0, 1)

    assert where(Z**2 <= 1).set == Interval(-1, 1)
    assert where(Z**2 <= 1).as_boolean() == Interval(-1, 1).as_relational(Z.symbol)
    assert where(And(X > Y, Y > 4)).as_boolean() == And(
        Eq(X.symbol, 6), Eq(Y.symbol, 5))

    assert len(where(X < 3).set) == 2
    assert 1 in where(X < 3).set

    X, Y = Normal('X', 0, 1), Normal('Y', 0, 1)
    assert where(And(X**2 <= 1, X >= 0)).set == Interval(0, 1)
    XX = given(X, And(X**2 <= 1, X >= 0))
    assert XX.pspace.domain.set == Interval(0, 1)
    assert XX.pspace.domain.as_boolean() == \
        And(0 <= X.symbol, X.symbol**2 <= 1, -oo < X.symbol, X.symbol < oo)

    with raises(TypeError):
        XX = given(X, X + 3)


def test_where() -> None:
    # https://github.com/pandas-dev/pandas/pull/63439
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    expr = pd.col("a").where(pd.col("b") == 5, 100)
    expected_str = "col('a').where(col('b') == 5, 100)"
    assert str(expr) == expected_str, str(expr)

    result = df.assign(c=expr)
    expected = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [100, 2, 100]})
    tm.assert_frame_equal(result, expected)

    expr = pd.col("a").where(pd.col("b") == 5, pd.col("a") + 1)
    expected_str = "col('a').where(col('b') == 5, col('a') + 1)"
    assert str(expr) == expected_str, str(expr)

    result = df.assign(c=expr)
    expected = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [2, 2, 4]})
    tm.assert_frame_equal(result, expected)


def test_where():
    s = Series(np.random.default_rng(2).standard_normal(5))
    cond = s > 0

    rs = s.where(cond).dropna()
    rs2 = s[cond]
    tm.assert_series_equal(rs, rs2)

    rs = s.where(cond, -s)
    tm.assert_series_equal(rs, s.abs())

    rs = s.where(cond)
    assert s.shape == rs.shape
    assert rs is not s

    # test alignment
    cond = Series([True, False, False, True, False], index=s.index)
    s2 = -(s.abs())

    expected = s2[cond].reindex(s2.index[:3]).reindex(s2.index)
    rs = s2.where(cond[:3])
    tm.assert_series_equal(rs, expected)

    expected = s2.abs()
    expected.iloc[0] = s2[0]
    rs = s2.where(cond[:3], -s2)
    tm.assert_series_equal(rs, expected)


def test_where(string_list, na_object):
    dtype = get_dtype(na_object)
    a = np.array(string_list, dtype=dtype)
    b = a[::-1]
    res = np.where([True, False, True, False, True, False], a, b)
    assert_array_equal(res, [a[0], b[1], a[2], b[3], a[4], b[5]])

