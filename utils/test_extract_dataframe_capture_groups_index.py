
def test_extract_dataframe_capture_groups_index(index, any_string_dtype):
    # GH6348
    # not passing index to the extractor

    data = ["A1", "B2", "C"]

    if len(index) < len(data):
        pytest.skip(f"Index needs more than {len(data)} values")

    index = index[: len(data)]
    s = Series(data, index=index, dtype=any_string_dtype)

    result = s.str.extract(r"(\d)", expand=True)
    expected = DataFrame(["1", "2", np.nan], index=index, dtype=any_string_dtype)
    tm.assert_frame_equal(result, expected)

    result = s.str.extract(r"(?P<letter>\D)(?P<number>\d)?", expand=True)
    expected = DataFrame(
        [["A", "1"], ["B", "2"], ["C", np.nan]],
        columns=["letter", "number"],
        index=index,
        dtype=any_string_dtype,
    )
    tm.assert_frame_equal(result, expected)

