
def test_rank():
    m = Matrix([[1, 2], [x, 1 - 1/x]])
    assert m.rank() == 2
    n = Matrix(3, 3, range(1, 10))
    assert n.rank() == 2
    p = zeros(3)
    assert p.rank() == 0


def test_rank():
    m = Matrix([[1, 2], [x, 1 - 1/x]])
    assert m.rank() == 2
    n = Matrix(3, 3, range(1, 10))
    assert n.rank() == 2
    p = zeros(3)
    assert p.rank() == 0


def test_rank(score, expected_rank):
    if hasattr(expected_rank, '__call__') and isinstance(
        expected_rank(), Exception
    ):
        with pytest.raises(expected_rank):
            cc_rank(score)
    else:
        assert cc_rank(score) == expected_rank


def test_rank(window, method, pct, ascending, test_data):
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

    expected = ser.expanding(window).apply(
        lambda x: x.rank(method=method, pct=pct, ascending=ascending).iloc[-1]
    )
    result = ser.expanding(window).rank(method=method, pct=pct, ascending=ascending)

    tm.assert_series_equal(result, expected)


def test_rank(window, method, pct, ascending, test_data):
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

    expected = ser.rolling(window).apply(
        lambda x: x.rank(method=method, pct=pct, ascending=ascending).iloc[-1]
    )
    result = ser.rolling(window).rank(method=method, pct=pct, ascending=ascending)

    tm.assert_series_equal(result, expected)

