
def test_scalarmappable_nan_to_rgba(bytes):
    sm = cm.ScalarMappable()

    # RGBA
    x = np.ones((2, 3, 4), dtype=float) * 0.5
    x[0, 0, 0] = np.nan
    expected = x.copy()
    expected[0, 0, :] = 0
    if bytes:
        expected = (expected * 255).astype(np.uint8)
    np.testing.assert_almost_equal(sm.to_rgba(x, bytes=bytes), expected)
    assert np.any(np.isnan(x))  # Input array should not be changed

    # RGB
    expected[..., 3] = 255 if bytes else 1
    expected[0, 0, 3] = 0
    np.testing.assert_almost_equal(sm.to_rgba(x[..., :3], bytes=bytes), expected)
    assert np.any(np.isnan(x))  # Input array should not be changed

    # Out-of-range fail
    x[1, 0, 0] = 42
    with pytest.raises(ValueError, match=r'\[0,1\] range'):
        sm.to_rgba(x[..., :3], bytes=bytes)

