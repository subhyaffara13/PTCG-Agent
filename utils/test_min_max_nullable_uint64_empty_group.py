
def test_min_max_nullable_uint64_empty_group():
    # don't raise NotImplementedError from libgroupby
    cat = pd.Categorical([0] * 10, categories=[0, 1])
    df = DataFrame({"A": cat, "B": pd.array(np.arange(10, dtype=np.uint64))})
    gb = df.groupby("A", observed=False)

    res = gb.min()

    idx = pd.CategoricalIndex([0, 1], dtype=cat.dtype, name="A")
    expected = DataFrame({"B": pd.array([0, pd.NA], dtype="UInt64")}, index=idx)
    tm.assert_frame_equal(res, expected)

    res = gb.max()
    expected.iloc[0, 0] = 9
    tm.assert_frame_equal(res, expected)

