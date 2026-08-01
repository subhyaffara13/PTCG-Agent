
def test_stack_positional_level_duplicate_column_names(future_stack):
    # https://github.com/pandas-dev/pandas/issues/36353
    columns = MultiIndex.from_product([("x", "y"), ("y", "z")], names=["a", "a"])
    df = DataFrame([[1, 1, 1, 1]], columns=columns)
    result = df.stack(0, future_stack=future_stack)

    new_columns = Index(["y", "z"], name="a")
    new_index = MultiIndex(
        levels=[range(1), ["x", "y"]], codes=[[0, 0], [0, 1]], names=[None, "a"]
    )
    expected = DataFrame([[1, 1], [1, 1]], index=new_index, columns=new_columns)

    tm.assert_frame_equal(result, expected)

