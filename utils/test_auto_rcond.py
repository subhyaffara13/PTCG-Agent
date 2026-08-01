
def test_auto_rcond(scale, pinv_):
    x = np.array([[1, 0], [0, 1e-10]]) * scale
    expected = np.diag(1. / np.diag(x))
    x_inv = pinv_(x)
    assert_allclose(x_inv, expected)

