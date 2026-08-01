
def test_pathlib_path_division(any_string_dtype, request):
    # GH#61940
    if any_string_dtype == object:
        mark = pytest.mark.xfail(
            reason="with NA present we go through _masked_arith_op which "
            "raises TypeError bc Path is not recognized by lib.is_scalar."
        )
        request.applymarker(mark)

    item = Path("/Users/Irv/")
    ser = Series(["A", "B", NA], dtype=any_string_dtype)

    result = item / ser
    expected = Series([item / "A", item / "B", ser.dtype.na_value], dtype=object)
    tm.assert_series_equal(result, expected)

    result = ser / item
    expected = Series(["A" / item, "B" / item, ser.dtype.na_value], dtype=object)
    tm.assert_series_equal(result, expected)

