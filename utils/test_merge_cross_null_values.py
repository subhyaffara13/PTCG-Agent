
def test_merge_cross_null_values(nulls_fixture):
    # GH#5401
    left = DataFrame({"a": [1, nulls_fixture]})
    right = DataFrame({"b": ["a", "b"], "c": [1.0, 2.0]})
    result = merge(left, right, how="cross")
    expected = DataFrame(
        {
            "a": [1, 1, nulls_fixture, nulls_fixture],
            "b": ["a", "b", "a", "b"],
            "c": [1.0, 2.0, 1.0, 2.0],
        }
    )
    tm.assert_frame_equal(result, expected)

