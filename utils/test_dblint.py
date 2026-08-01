
def test_dblint(k):
    # Basic test to see it runs and gives the correct result on a trivial
    # problem. Note that `dblint` is not exposed in the interpolate namespace.
    x = np.linspace(0, 1)
    y = np.linspace(0, 1)
    xx, yy = np.meshgrid(x, y)
    rect = RectBivariateSpline(x, y, 4 * xx * yy,
                               kx=k, ky=k)
    rect_custom = _regrid(x, y, 4 * xx * yy,
                                              kx=k, ky=k)
    tck = list(rect.tck)
    tck.extend(rect.degrees)
    tck_custom = list(rect_custom.t + (rect_custom.c.flatten(),))
    tck_custom.extend(rect.degrees)

    assert abs(dblint(0, 1, 0, 1, tck) - 1) < 1e-10
    assert abs(dblint(0, 1, 0, 1, tck_custom) - 1) < 1e-10

    assert abs(dblint(0, 0.5, 0, 1, tck) - 0.25) < 1e-10
    assert abs(dblint(0, 0.5, 0, 1, tck_custom) - 0.25) < 1e-10

    assert abs(dblint(0.5, 1, 0, 1, tck) - 0.75) < 1e-10
    assert abs(dblint(0.5, 1, 0, 1, tck_custom) - 0.75) < 1e-10

    assert abs(dblint(-100, 100, -100, 100, tck) - 1) < 1e-10
    assert abs(dblint(-100, 100, -100, 100, tck_custom) - 1) < 1e-10

