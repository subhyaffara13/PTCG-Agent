
def test_normalize(form, expected, any_string_dtype):
    ser = Series(
        ["ABC", "ＡＢＣ", "１２３", np.nan, "ｱｲｴ"],  # noqa: RUF001
        index=["a", "b", "c", "d", "e"],
        dtype=any_string_dtype,
    )
    expected = Series(expected, index=["a", "b", "c", "d", "e"], dtype=any_string_dtype)
    result = ser.str.normalize(form)
    tm.assert_series_equal(result, expected)

