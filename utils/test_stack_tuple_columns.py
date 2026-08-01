
def test_stack_tuple_columns(future_stack):
    # GH#54948 - test stack when the input has a non-MultiIndex with tuples
    df = DataFrame(
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]], columns=[("a", 1), ("a", 2), ("b", 1)]
    )
    result = df.stack(future_stack=future_stack)
    expected = Series(
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        index=MultiIndex(
            levels=[range(3), [("a", 1), ("a", 2), ("b", 1)]],
            codes=[[0, 0, 0, 1, 1, 1, 2, 2, 2], [0, 1, 2, 0, 1, 2, 0, 1, 2]],
        ),
    )
    tm.assert_series_equal(result, expected)

