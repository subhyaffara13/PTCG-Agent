
def test_mgr_locs_updated(func):
    # https://github.com/pandas-dev/pandas/issues/31802
    # Some operations may require creating new blocks, which requires
    # valid mgr_locs
    df = pd.DataFrame({"A": ["a", "a", "a"], "B": ["a", "b", "b"], "C": [1, 1, 1]})
    result = df.groupby(["A", "B"]).agg(func)
    expected = pd.DataFrame(
        {"C": [0, 0]},
        index=pd.MultiIndex.from_product([["a"], ["a", "b"]], names=["A", "B"]),
    )
    tm.assert_frame_equal(result, expected)

