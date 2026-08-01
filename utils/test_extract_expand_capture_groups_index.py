
def test_extract_expand_capture_groups_index(index, any_string_dtype):
    # https://github.com/pandas-dev/pandas/issues/6348
    # not passing index to the extractor
    data = ["A1", "B2", "C"]

    if len(index) == 0:
        pytest.skip("Test requires len(index) > 0")
    while len(index) < len(data):
        index = index.repeat(2)

    index = index[: len(data)]
    ser = Series(data, index=index, dtype=any_string_dtype)

    result = ser.str.extract(r"(\d)", expand=False)
    expected = Series(["1", "2", np.nan], index=index, dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

    result = ser.str.extract(r"(?P<letter>\D)(?P<number>\d)?", expand=False)
    expected = DataFrame(
        [["A", "1"], ["B", "2"], ["C", np.nan]],
        columns=["letter", "number"],
        index=index,
        dtype=any_string_dtype,
    )
    tm.assert_frame_equal(result, expected)

