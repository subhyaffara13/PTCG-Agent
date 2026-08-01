
def test_segment_hits():
    """Test a problematic case."""
    cx, cy = 553, 902
    x, y = np.array([553., 553.]), np.array([95., 947.])
    radius = 6.94
    assert_array_equal(mlines.segment_hits(cx, cy, x, y, radius), [0])

