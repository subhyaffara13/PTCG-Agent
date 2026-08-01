
def test_unstack_non_slice_like_blocks():
    # Case where the mgr_locs of a DataFrame's underlying blocks are not slice-like

    mi = MultiIndex.from_product([range(5), ["A", "B", "C"]])
    df = DataFrame(
        {
            0: np.random.default_rng(2).standard_normal(15),
            1: np.random.default_rng(2).standard_normal(15).astype(np.int64),
            2: np.random.default_rng(2).standard_normal(15),
            3: np.random.default_rng(2).standard_normal(15),
        },
        index=mi,
    )
    assert any(not x.mgr_locs.is_slice_like for x in df._mgr.blocks)

    res = df.unstack()

    expected = pd.concat([df[n].unstack() for n in range(4)], keys=range(4), axis=1)
    tm.assert_frame_equal(res, expected)

