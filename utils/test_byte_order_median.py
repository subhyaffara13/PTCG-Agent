
def test_byte_order_median():
    """Regression test for #413: median_filter does not handle bytes orders."""
    a = np.arange(9, dtype='<f4').reshape(3, 3)
    ref = ndimage.median_filter(a, (3, 3))
    b = np.arange(9, dtype='>f4').reshape(3, 3)
    t = ndimage.median_filter(b, (3, 3))
    assert_array_almost_equal(ref, t)

