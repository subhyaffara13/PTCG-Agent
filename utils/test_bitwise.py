
def test_bitwise(pa_type):
    # GH 54495
    dtype = ArrowDtype(pa_type)
    left = pd.Series([1, None, 3, 4], dtype=dtype)
    right = pd.Series([None, 3, 5, 4], dtype=dtype)

    result = left | right
    expected = pd.Series([None, None, 3 | 5, 4 | 4], dtype=dtype)
    tm.assert_series_equal(result, expected)

    result = left & right
    expected = pd.Series([None, None, 3 & 5, 4 & 4], dtype=dtype)
    tm.assert_series_equal(result, expected)

    result = left ^ right
    expected = pd.Series([None, None, 3 ^ 5, 4 ^ 4], dtype=dtype)
    tm.assert_series_equal(result, expected)

    result = ~left
    expected = ~(left.fillna(0).to_numpy())
    expected = pd.Series(expected, dtype=dtype).mask(left.isnull())
    tm.assert_series_equal(result, expected)


def test_bitwise(dtype):
    left = pd.array([1, None, 3, 4], dtype=dtype)
    right = pd.array([None, 3, 5, 4], dtype=dtype)

    with pytest.raises(TypeError, match="unsupported operand type"):
        left | right
    with pytest.raises(TypeError, match="unsupported operand type"):
        left & right
    with pytest.raises(TypeError, match="unsupported operand type"):
        left ^ right


def test_bitwise(dtype):
    left = pd.array([1, None, 3, 4], dtype=dtype)
    right = pd.array([None, 3, 5, 4], dtype=dtype)

    result = left | right
    expected = pd.array([None, None, 3 | 5, 4 | 4], dtype=dtype)
    tm.assert_extension_array_equal(result, expected)

    result = left & right
    expected = pd.array([None, None, 3 & 5, 4 & 4], dtype=dtype)
    tm.assert_extension_array_equal(result, expected)

    result = left ^ right
    expected = pd.array([None, None, 3 ^ 5, 4 ^ 4], dtype=dtype)
    tm.assert_extension_array_equal(result, expected)

    # TODO: desired behavior when operating with boolean?  defer?

    floats = right.astype("Float64")
    with pytest.raises(TypeError, match="unsupported operand type"):
        left | floats
    with pytest.raises(TypeError, match="unsupported operand type"):
        left & floats
    with pytest.raises(TypeError, match="unsupported operand type"):
        left ^ floats

