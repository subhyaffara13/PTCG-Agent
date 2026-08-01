
def test_spline_filter_reflect_small_n(order, n, xp):
    # Regression test for gh-24550: the causal reflect initialization had an
    # aliasing bug where c[0] was read back after mutation via c[n-1-i].
    # For large n the error is negligible, but for small n it is significant.
    eye = xp.eye(n, dtype=xp.float64)
    filtered = ndimage.spline_filter1d(eye, axis=0, order=order, mode='reflect')
    matrix = make_spline_knot_matrix(xp, n, order, mode='reflect')
    xp_assert_close(filtered @ matrix, eye, atol=1e-12)

