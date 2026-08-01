
def test_truncate(kwargs):
    df = DataFrame({"a": [1, 2, 3], "b": 1, "c": 2})
    df_orig = df.copy()
    df2 = df.truncate(**kwargs)
    df2._mgr._verify_integrity()

    assert np.shares_memory(get_array(df2, "a"), get_array(df, "a"))

    df2.iloc[0, 0] = 0
    assert not np.shares_memory(get_array(df2, "a"), get_array(df, "a"))
    tm.assert_frame_equal(df, df_orig)


def test_truncate(Poly):
    p = Poly([1, 2, 3])
    assert_raises(ValueError, p.truncate, .5)
    assert_raises(ValueError, p.truncate, 0)
    assert_equal(len(p.truncate(4)), 3)
    assert_equal(len(p.truncate(3)), 3)
    assert_equal(len(p.truncate(2)), 2)
    assert_equal(len(p.truncate(1)), 1)

