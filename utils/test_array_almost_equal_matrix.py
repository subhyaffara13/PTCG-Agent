
def test_array_almost_equal_matrix():
    # Matrix slicing keeps things 2-D, while array does not necessarily.
    # See gh-8452.
    # 2018-04-29: moved here from testing.tests.test_utils.
    m1 = np.matrix([[1., 2.]])
    m2 = np.matrix([[1., np.nan]])
    m3 = np.matrix([[1., -np.inf]])
    m4 = np.matrix([[np.nan, np.inf]])
    m5 = np.matrix([[1., 2.], [np.nan, np.inf]])
    for assert_func in assert_array_almost_equal, assert_almost_equal:
        for m in m1, m2, m3, m4, m5:
            assert_func(m, m)
            a = np.array(m)
            assert_func(a, m)
            assert_func(m, a)

