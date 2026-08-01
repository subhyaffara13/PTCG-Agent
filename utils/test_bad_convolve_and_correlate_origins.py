
def test_bad_convolve_and_correlate_origins(xp):
    """Regression test for gh-822."""
    # Before gh-822 was fixed, these would generate seg. faults or
    # other crashes on many system.
    assert_raises(ValueError, ndimage.correlate1d,
                  [0, 1, 2, 3, 4, 5], [1, 1, 2, 0], origin=2)
    assert_raises(ValueError, ndimage.correlate,
                  [0, 1, 2, 3, 4, 5], [0, 1, 2], origin=[2])
    assert_raises(ValueError, ndimage.correlate,
                  xp.ones((3, 5)), xp.ones((2, 2)), origin=[0, 1])

    assert_raises(ValueError, ndimage.convolve1d,
                  xp.arange(10), xp.ones(3), origin=-2)
    assert_raises(ValueError, ndimage.convolve,
                  xp.arange(10), xp.ones(3), origin=[-2])
    assert_raises(ValueError, ndimage.convolve,
                  xp.ones((3, 5)), xp.ones((2, 2)), origin=[0, -2])

