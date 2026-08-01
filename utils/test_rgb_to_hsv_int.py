
def test_rgb_to_hsv_int():
    # Test that int rgb values (still range 0-1) are processed correctly.
    assert_array_equal(mcolors.rgb_to_hsv((0, 1, 0)), (1/3, 1, 1))  # green

