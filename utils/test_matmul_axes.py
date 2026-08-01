
def test_matmul_axes():
    a = np.arange(3 * 4 * 5).reshape(3, 4, 5)
    c = np.matmul(a, a, axes=[(-2, -1), (-1, -2), (1, 2)])
    assert c.shape == (3, 4, 4)
    d = np.matmul(a, a, axes=[(-2, -1), (-1, -2), (0, 1)])
    assert d.shape == (4, 4, 3)
    e = np.swapaxes(d, 0, 2)
    assert_array_equal(e, c)
    f = np.matmul(a, np.arange(3), axes=[(1, 0), (0), (0)])
    assert f.shape == (4, 5)

