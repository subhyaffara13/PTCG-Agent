
def test_empty_pass_dtype(all_parsers):
    parser = all_parsers

    data = "one,two"
    result = parser.read_csv(StringIO(data), dtype={"one": "u1"})

    expected = DataFrame(
        {"one": np.empty(0, dtype="u1"), "two": np.empty(0, dtype=object)},
    )
    tm.assert_frame_equal(result, expected)

