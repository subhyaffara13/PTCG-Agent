
def test_pade_trivial():
    with pytest.warns(DeprecationWarning, match="`pade` is deprecated"):
        nump, denomp = pade([1.0], 0)
    xp_assert_equal(nump.c, np.asarray([1.0]))
    xp_assert_equal(denomp.c, np.asarray([1.0]))

    with pytest.warns(DeprecationWarning, match="`pade` is deprecated"):
        nump, denomp = pade([1.0], 0, 0)
    xp_assert_equal(nump.c, np.asarray([1.0]))
    xp_assert_equal(denomp.c, np.asarray([1.0]))

