
def test_join_multi():
    # GH 10665
    midx = MultiIndex.from_product([np.arange(4), np.arange(4)], names=["a", "b"])
    idx = Index([1, 2, 5], name="b")

    # inner
    jidx, lidx, ridx = midx.join(idx, how="inner", return_indexers=True)
    exp_idx = MultiIndex.from_product([np.arange(4), [1, 2]], names=["a", "b"])
    exp_lidx = np.array([1, 2, 5, 6, 9, 10, 13, 14], dtype=np.intp)
    exp_ridx = np.array([0, 1, 0, 1, 0, 1, 0, 1], dtype=np.intp)
    tm.assert_index_equal(jidx, exp_idx)
    tm.assert_numpy_array_equal(lidx, exp_lidx)
    tm.assert_numpy_array_equal(ridx, exp_ridx)
    # flip
    jidx, ridx, lidx = idx.join(midx, how="inner", return_indexers=True)
    tm.assert_index_equal(jidx, exp_idx)
    tm.assert_numpy_array_equal(lidx, exp_lidx)
    tm.assert_numpy_array_equal(ridx, exp_ridx)

    # keep MultiIndex
    jidx, lidx, ridx = midx.join(idx, how="left", return_indexers=True)
    exp_ridx = np.array(
        [-1, 0, 1, -1, -1, 0, 1, -1, -1, 0, 1, -1, -1, 0, 1, -1], dtype=np.intp
    )
    tm.assert_index_equal(jidx, midx)
    assert lidx is None
    tm.assert_numpy_array_equal(ridx, exp_ridx)
    # flip
    jidx, ridx, lidx = idx.join(midx, how="right", return_indexers=True)
    tm.assert_index_equal(jidx, midx)
    assert lidx is None
    tm.assert_numpy_array_equal(ridx, exp_ridx)

