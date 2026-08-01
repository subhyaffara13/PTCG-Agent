
def like_function():
    # 2018-04-29: moved here from core.tests.test_numeric
    a = np.matrix([[1, 2], [3, 4]])
    for like_function in np.zeros_like, np.ones_like, np.empty_like:
        b = like_function(a)
        assert_(type(b) is np.matrix)

        c = like_function(a, subok=False)
        assert_(type(c) is not np.matrix)

