
def test_str_starts_ends_with_all_nulls_empty_tuple(side):
    ser = pd.Series([None, None], dtype=ArrowDtype(pa.string()))
    result = getattr(ser.str, side)(())

    # bool datatype preserved for all nulls.
    expected = pd.Series([None, None], dtype=ArrowDtype(pa.bool_()))
    tm.assert_series_equal(result, expected)

