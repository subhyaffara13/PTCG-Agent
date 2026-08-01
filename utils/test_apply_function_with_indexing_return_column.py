
def test_apply_function_with_indexing_return_column():
    # GH#7002, GH#41480, GH#49256
    df = DataFrame(
        {
            "foo1": ["one", "two", "two", "three", "one", "two"],
            "foo2": [1, 2, 4, 4, 5, 6],
        }
    )
    result = df.groupby("foo1", as_index=False).apply(lambda x: x.mean())
    expected = DataFrame(
        {
            "foo1": ["one", "three", "two"],
            "foo2": [3.0, 4.0, 4.0],
        }
    )
    tm.assert_frame_equal(result, expected)

