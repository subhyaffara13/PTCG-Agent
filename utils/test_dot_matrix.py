
def test_dot_matrix():
    # Test to make sure matrices give the same answer as ndarrays
    # 2018-04-29: moved here from core.tests.test_function_base.
    x = np.linspace(0, 5)
    y = np.linspace(-5, 0)
    mx = np.matrix(x)
    my = np.matrix(y)
    r = np.dot(x, y)
    mr = np.dot(mx, my.T)
    assert_almost_equal(mr, r)

