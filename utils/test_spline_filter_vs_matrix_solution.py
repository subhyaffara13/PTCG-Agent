
def test_spline_filter_vs_matrix_solution(order, mode, xp):
    n = 100
    eye = xp.eye(n, dtype=xp.float64)
    spline_filter_axis_0 = ndimage.spline_filter1d(eye, axis=0, order=order,
                                                   mode=mode)
    spline_filter_axis_1 = ndimage.spline_filter1d(eye, axis=1, order=order,
                                                   mode=mode)
    matrix = make_spline_knot_matrix(xp, n, order, mode=mode)
    assert_almost_equal(eye, spline_filter_axis_0 @ matrix)
    assert_almost_equal(eye, spline_filter_axis_1 @ matrix.T)

