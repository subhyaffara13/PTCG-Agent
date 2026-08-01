
def test_exponential_backoff():
    # GH#55518
    df = DataFrame({"a": [1, 2, 3]})
    for i in range(490):
        df.copy(deep=False)

    assert len(df._mgr.blocks[0].refs.referenced_blocks) == 491

    df = DataFrame({"a": [1, 2, 3]})
    dfs = [df.copy(deep=False) for i in range(510)]

    for i in range(20):
        df.copy(deep=False)
    assert len(df._mgr.blocks[0].refs.referenced_blocks) == 531
    assert df._mgr.blocks[0].refs.clear_counter == 1000

    for i in range(500):
        df.copy(deep=False)

    # Don't reduce since we still have over 500 objects alive
    assert df._mgr.blocks[0].refs.clear_counter == 1000

    dfs = dfs[:300]
    for i in range(500):
        df.copy(deep=False)

    # Reduce since there are less than 500 objects alive
    assert df._mgr.blocks[0].refs.clear_counter == 500

