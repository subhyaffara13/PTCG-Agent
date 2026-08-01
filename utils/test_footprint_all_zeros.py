
def test_footprint_all_zeros(xp):
    # regression test for gh-6876: footprint of all zeros segfaults
    arr = xp.asarray(np.random.randint(0, 100, (100, 100)))
    kernel = xp.asarray(np.zeros((3, 3), dtype=bool))
    with assert_raises(ValueError):
        ndimage.maximum_filter(arr, footprint=kernel)

