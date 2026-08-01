
def test_nunique(index_or_series_obj):
    obj = index_or_series_obj
    obj = np.repeat(obj, range(1, len(obj) + 1))
    expected = len(obj.unique())
    assert obj.nunique(dropna=False) == expected


def test_nunique():
    df = DataFrame({"A": list("abbacc"), "B": list("abxacc"), "C": list("abbacx")})

    expected = DataFrame({"A": list("abc"), "B": [1, 2, 1], "C": [1, 1, 2]})
    result = df.groupby("A", as_index=False).nunique()
    tm.assert_frame_equal(result, expected)

    # as_index
    expected.index = list("abc")
    expected.index.name = "A"
    expected = expected.drop(columns="A")
    result = df.groupby("A").nunique()
    tm.assert_frame_equal(result, expected)

    # with na
    result = df.replace({"x": None}).groupby("A").nunique(dropna=False)
    tm.assert_frame_equal(result, expected)

    # dropna
    expected = DataFrame({"B": [1] * 3, "C": [1] * 3}, index=list("abc"))
    expected.index.name = "A"
    result = df.replace({"x": None}).groupby("A").nunique()
    tm.assert_frame_equal(result, expected)


def test_nunique(window, test_data):
    length = 20
    if test_data == "default":
        ser = Series(data=np.random.default_rng(2).random(length))
    elif test_data == "duplicates":
        ser = Series(data=np.random.default_rng(2).choice(3, length))
    elif test_data == "nans":
        ser = Series(
            data=np.random.default_rng(2).choice(
                [1.0, 0.25, 0.75, np.nan, np.inf, -np.inf], length
            )
        )
    elif test_data == "precision":
        ser = Series(
            data=[
                0.3,
                0.1 * 3,  # Not necessarily exactly 0.3
                0.6,
                0.2 * 3,  # Not necessarily exactly 0.6
                0.9,
                0.3 * 3,  # Not necessarily exactly 0.9
                0.5,
                0.1 * 5,  # Not necessarily exactly 0.5
                0.8,
                0.2 * 4,  # Not necessarily exactly 0.8
            ],
            dtype=np.float64,
        )

    expected = ser.expanding(window).apply(lambda x: x.nunique())
    result = ser.expanding(window).nunique()

    tm.assert_series_equal(result, expected)


def test_nunique(window, test_data):
    length = 20
    if test_data == "default":
        ser = Series(data=np.random.default_rng(2).random(length))
    elif test_data == "duplicates":
        ser = Series(data=np.random.default_rng(2).choice(3, length))
    elif test_data == "nans":
        ser = Series(
            data=np.random.default_rng(2).choice(
                [1.0, 0.25, 0.75, np.nan, np.inf, -np.inf], length
            )
        )
    elif test_data == "precision":
        ser = Series(
            data=[
                0.3,
                0.1 * 3,  # Not necessarily exactly 0.3
                0.6,
                0.2 * 3,  # Not necessarily exactly 0.6
                0.9,
                0.3 * 3,  # Not necessarily exactly 0.9
                0.5,
                0.1 * 5,  # Not necessarily exactly 0.5
                0.8,
                0.2 * 4,  # Not necessarily exactly 0.8
            ],
            dtype=np.float64,
        )

    expected = ser.rolling(window).apply(lambda x: x.nunique())
    result = ser.rolling(window).nunique()

    tm.assert_series_equal(result, expected)


def test_nunique():
    # basics.rst doc example
    series = Series(np.random.default_rng(2).standard_normal(500))
    series[20:500] = np.nan
    series[10:20] = 5000
    result = series.nunique()
    assert result == 11

