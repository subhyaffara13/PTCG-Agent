
def test_indexing(xp):
    atol = 1e-12

    # Test indexing for multiple transforms
    r = Rotation.from_euler('zyx', xp.asarray([[90, 0, 0], [0, 90, 0]]), degrees=True)
    t = xp.asarray([[1.0, 2, 3], [4, 5, 6]])
    tf = RigidTransform.from_components(t, r)

    # Test single index
    xp_assert_close(tf[0].as_matrix()[:3, :3], r[0].as_matrix(), atol=atol)
    xp_assert_close(tf[0].as_matrix()[:3, 3], t[0, ...], atol=atol)

    # Test slice
    tf_slice = tf[0:2]
    xp_assert_close(tf_slice.as_matrix()[:, :3, :3], r[0:2].as_matrix(), atol=atol)
    xp_assert_close(tf_slice.as_matrix()[:, :3, 3], t[0:2, ...], atol=atol)

    # Test boolean indexing
    tf_masked = tf[xp.asarray([True, True])]
    xp_assert_close(tf_masked.as_matrix()[:, :3, :3], r.as_matrix(), atol=atol)
    xp_assert_close(tf_masked.as_matrix()[:, :3, 3], t, atol=atol)

    tf_masked = tf[xp.asarray([False, True])]
    xp_assert_close(tf_masked.as_matrix()[:, :3, :3],
                    r[xp.asarray([False, True])].as_matrix(), atol=atol)
    xp_assert_close(tf_masked.as_matrix()[:, :3, 3], t[xp.asarray([False, True])],
                    atol=atol)

    tf_masked = tf[xp.asarray([False, False])]
    assert len(tf_masked) == 0

    # Test integer array indexing
    idx = xp.asarray([0, 1])
    xp_assert_close(tf[idx].as_matrix()[:, :3, :3], r[idx].as_matrix(), atol=atol)
    xp_assert_close(tf[idx].as_matrix()[:, :3, 3], t, atol=atol)


def test_indexing(A):
    if A.__class__.__name__[:3] in ('dia', 'coo', 'bsr'):
        return

    all_res = (
        A[1, :],
        A[:, 1],
        A[1, [1, 2]],
        A[[1, 2], 1],
        A[[0]],
        A[:, [1, 2]],
        A[[1, 2], :],
        A[1, [[1, 2]]],
        A[[[1, 2]], 1],
    )

    for res in all_res:
        assert isinstance(res, scipy.sparse.sparray), \
            f"Expected sparse array, got {res._class__.__name__}"


def test_indexing():
    idx = date_range("2001-1-1", periods=20, freq="ME")
    ts = Series(np.random.default_rng(2).random(len(idx)), index=idx)

    # getting

    # GH 3070, make sure semantics work on Series/Frame
    result = ts["2001"]
    tm.assert_series_equal(result, ts.iloc[:12])

    df = DataFrame({"A": ts})

    # GH#36179 pre-2.0 df["2001"] operated as slicing on rows. in 2.0 it behaves
    #  like any other key, so raises
    with pytest.raises(KeyError, match="2001"):
        df["2001"]

    # setting
    ts = Series(np.random.default_rng(2).random(len(idx)), index=idx)
    expected = ts.copy()
    expected.iloc[:12] = 1
    ts["2001"] = 1
    tm.assert_series_equal(ts, expected)

    expected = df.copy()
    expected.iloc[:12, 0] = 1
    df.loc["2001", "A"] = 1
    tm.assert_frame_equal(df, expected)

