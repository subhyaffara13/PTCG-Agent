
def test_scalarmappable_to_rgba(bytes):
    sm = cm.ScalarMappable()
    alpha_1 = 255 if bytes else 1

    # uint8 RGBA
    x = np.ones((2, 3, 4), dtype=np.uint8)
    expected = x.copy() if bytes else x.astype(np.float32)/255
    np.testing.assert_almost_equal(sm.to_rgba(x, bytes=bytes), expected)
    # uint8 RGB
    expected[..., 3] = alpha_1
    np.testing.assert_almost_equal(sm.to_rgba(x[..., :3], bytes=bytes), expected)
    # uint8 masked RGBA
    xm = np.ma.masked_array(x, mask=np.zeros_like(x))
    xm.mask[0, 0, 0] = True
    expected = x.copy() if bytes else x.astype(np.float32)/255
    expected[0, 0, 3] = 0
    np.testing.assert_almost_equal(sm.to_rgba(xm, bytes=bytes), expected)
    # uint8 masked RGB
    expected[..., 3] = alpha_1
    expected[0, 0, 3] = 0
    np.testing.assert_almost_equal(sm.to_rgba(xm[..., :3], bytes=bytes), expected)

    # float RGBA
    x = np.ones((2, 3, 4), dtype=float) * 0.5
    expected = (x * 255).astype(np.uint8) if bytes else x.copy()
    np.testing.assert_almost_equal(sm.to_rgba(x, bytes=bytes), expected)
    # float RGB
    expected[..., 3] = alpha_1
    np.testing.assert_almost_equal(sm.to_rgba(x[..., :3], bytes=bytes), expected)
    # float masked RGBA
    xm = np.ma.masked_array(x, mask=np.zeros_like(x))
    xm.mask[0, 0, 0] = True
    expected = (x * 255).astype(np.uint8) if bytes else x.copy()
    expected[0, 0, 3] = 0
    np.testing.assert_almost_equal(sm.to_rgba(xm, bytes=bytes), expected)
    # float masked RGB
    expected[..., 3] = alpha_1
    expected[0, 0, 3] = 0
    np.testing.assert_almost_equal(sm.to_rgba(xm[..., :3], bytes=bytes), expected)

