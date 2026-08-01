
def test_update_inplace_sets_valid_block_values():
    # https://github.com/pandas-dev/pandas/issues/33457
    df = DataFrame({"a": Series([1, 2, None], dtype="category")})

    # inplace update of a single column
    with tm.raises_chained_assignment_error():
        df["a"].fillna(1, inplace=True)

    # check we haven't put a Series into any block.values
    assert isinstance(df._mgr.blocks[0].values, Categorical)

