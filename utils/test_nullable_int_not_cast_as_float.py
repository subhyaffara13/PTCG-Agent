
def test_nullable_int_not_cast_as_float(method, dtype, val):
    data = [val, pd.NA]
    df = DataFrame({"grp": [1, 1], "b": data}, dtype=dtype)
    grouped = df.groupby("grp")

    result = grouped.transform(method)
    expected = DataFrame({"b": data}, dtype=dtype)

    tm.assert_frame_equal(result, expected)

