
def test_count():
    assert count((1, 2, 3)) == 3
    assert count([]) == 0
    assert count(iter((1, 2, 3, 4))) == 4

    assert count('hello') == 5
    assert count(iter('hello')) == 5


def test_count():
    expr = (x + y + 2 + sin(3*x))

    assert expr.count(lambda u: u.is_Integer) == 2
    assert expr.count(lambda u: u.is_Symbol) == 3

    assert expr.count(Integer) == 2
    assert expr.count(Symbol) == 3
    assert expr.count(2) == 1

    a = Wild('a')

    assert expr.count(sin) == 1
    assert expr.count(sin(a)) == 1
    assert expr.count(lambda u: type(u) is sin) == 1

    assert f(x).count(f(x)) == 1
    assert f(x).diff(x).count(f(x)) == 1
    assert f(x).diff(x).count(x) == 2


def test_count():
    n = 1 << 15
    dr = date_range("2015-08-30", periods=n // 10, freq="min")

    df = DataFrame(
        {
            "1st": np.random.default_rng(2).choice(list(ascii_lowercase), n),
            "2nd": np.random.default_rng(2).integers(0, 5, n),
            "3rd": np.random.default_rng(2).standard_normal(n).round(3),
            "4th": np.random.default_rng(2).integers(-10, 10, n),
            "5th": np.random.default_rng(2).choice(dr, n),
            "6th": np.random.default_rng(2).standard_normal(n).round(3),
            "7th": np.random.default_rng(2).standard_normal(n).round(3),
            "8th": np.random.default_rng(2).choice(dr, n)
            - np.random.default_rng(2).choice(dr, 1),
            "9th": np.random.default_rng(2).choice(list(ascii_lowercase), n),
        }
    )

    for col in df.columns.drop(["1st", "2nd", "4th"]):
        df.loc[np.random.default_rng(2).choice(n, n // 10), col] = np.nan

    df["9th"] = df["9th"].astype("category")

    for key in ["1st", "2nd", ["1st", "2nd"]]:
        left = df.groupby(key).count()
        right = df.groupby(key).apply(DataFrame.count)
        tm.assert_frame_equal(left, right)


def test_count(test_series):
    test_series[::3] = np.nan

    expected = test_series.groupby(lambda x: x.year).count()

    grouper = Grouper(freq="YE", label="right", closed="right")
    result = test_series.groupby(grouper).count()
    expected.index = result.index
    tm.assert_series_equal(result, expected)

    result = test_series.resample("YE").count()
    expected.index = result.index
    tm.assert_series_equal(result, expected)


def test_count(any_string_dtype):
    ser = Series(["foo", "foofoo", np.nan, "foooofooofommmfoo"], dtype=any_string_dtype)
    result = ser.str.count("f[o]+")
    if is_object_or_nan_string_dtype(any_string_dtype):
        expected_dtype = np.float64
        item = np.nan
    else:
        expected_dtype = "Int64"
        item = NA

    expected = Series([1, 2, item, 4], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

