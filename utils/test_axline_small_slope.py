
def test_axline_small_slope():
    """Test that small slopes are not coerced to zero in the transform."""
    line = plt.axline((0, 0), slope=1e-14)
    p1 = line.get_transform().transform_point((0, 0))
    p2 = line.get_transform().transform_point((1, 1))
    # y-values must be slightly different
    dy = p2[1] - p1[1]
    assert dy > 0
    assert dy < 4e-12

