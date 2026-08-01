
def test_where_unsafe_upcast(dtype, expected_dtype):
    # see gh-9743
    s = Series(np.arange(10), dtype=dtype)
    values = [2.5, 3.5, 4.5, 5.5, 6.5]
    mask = s < 5
    if np.dtype(dtype).kind == np.dtype(expected_dtype).kind == "f":
        s[mask] = values
        expected = Series(values + list(range(5, 10)), dtype=expected_dtype)
        tm.assert_series_equal(s, expected)
    else:
        with pytest.raises(TypeError, match="Invalid value"):
            s[mask] = values

