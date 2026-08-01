
def test_infer_types_boolean_sum(all_parsers):
    # GH#44079
    parser = all_parsers
    result = parser.read_csv(
        StringIO("0,1"),
        names=["a", "b"],
        index_col=["a"],
        dtype={"a": "UInt8"},
    )
    expected = DataFrame(
        data={
            "a": [
                0,
            ],
            "b": [1],
        }
    ).set_index("a")
    # Not checking index type now, because the C parser will return a
    # index column of dtype 'object', and the Python parser will return a
    # index column of dtype 'int64'.
    tm.assert_frame_equal(result, expected, check_index_type=False)

