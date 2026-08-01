
def test_map_series_stringdtype(any_string_dtype, using_infer_string):
    # map test on StringDType, GH#40823
    ser1 = Series(
        data=["cat", "dog", "rabbit"],
        index=["id1", "id2", "id3"],
        dtype=any_string_dtype,
    )
    ser2 = Series(["id3", "id2", "id1", "id7000"], dtype=any_string_dtype)
    result = ser2.map(ser1)

    item = pd.NA
    if ser2.dtype == object:
        item = np.nan

    expected = Series(data=["rabbit", "dog", "cat", item], dtype=any_string_dtype)
    if using_infer_string and any_string_dtype == "object":
        expected = expected.astype("str")

    tm.assert_series_equal(result, expected)

