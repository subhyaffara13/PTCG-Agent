
def test_first_last_skipna(any_real_nullable_dtype, sort, skipna, how):
    # GH#57019
    na_value = na_value_for_dtype(pandas_dtype(any_real_nullable_dtype))
    df = DataFrame(
        {
            "a": [2, 1, 1, 2, 3, 3],
            # TODO: test that has mixed na_value and NaN either working for
            #  float or raising for int?
            "b": [na_value, 3.0, na_value, 4.0, na_value, na_value],
            "c": [na_value, 3.0, na_value, 4.0, na_value, na_value],
        },
        dtype=any_real_nullable_dtype,
    )
    gb = df.groupby("a", sort=sort)
    method = getattr(gb, how)
    result = method(skipna=skipna)

    ilocs = {
        ("first", True): [3, 1, 4],
        ("first", False): [0, 1, 4],
        ("last", True): [3, 1, 5],
        ("last", False): [3, 2, 5],
    }[how, skipna]
    expected = df.iloc[ilocs].set_index("a")
    if sort:
        expected = expected.sort_index()
    tm.assert_frame_equal(result, expected)


def test_first_last_skipna(any_real_nullable_dtype, skipna, how):
    # GH#57019
    if is_extension_array_dtype(any_real_nullable_dtype):
        na_value = Series(dtype=any_real_nullable_dtype).dtype.na_value
    else:
        na_value = np.nan
    df = DataFrame(
        {
            "a": [2, 1, 1, 2],
            "b": [na_value, 3.0, na_value, 4.0],
            "c": [na_value, 3.0, na_value, 4.0],
        },
        index=date_range("2020-01-01", periods=4, freq="D", unit="ns"),
        dtype=any_real_nullable_dtype,
    )
    rs = df.resample("ME")
    method = getattr(rs, how)
    result = method(skipna=skipna)

    ts = pd.to_datetime("2020-01-31").as_unit("ns")
    gb = df.groupby(df.shape[0] * [ts])
    expected = getattr(gb, how)(skipna=skipna)
    expected.index.freq = "ME"
    tm.assert_frame_equal(result, expected)

