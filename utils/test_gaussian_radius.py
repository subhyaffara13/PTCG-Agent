
def test_gaussian_radius(xp):
    # Test that Gaussian filters with radius argument produce the same
    # results as the filters with corresponding truncate argument.
    # radius = int(truncate * sigma + 0.5)
    # Test gaussian_filter1d
    x = np.zeros(7)
    x[3] = 1
    x = xp.asarray(x)
    f1 = ndimage.gaussian_filter1d(x, sigma=2, truncate=1.5)
    f2 = ndimage.gaussian_filter1d(x, sigma=2, radius=3)
    xp_assert_equal(f1, f2)

    # Test gaussian_filter when sigma is a number.
    a = np.zeros((9, 9))
    a[4, 4] = 1
    a = xp.asarray(a)
    f1 = ndimage.gaussian_filter(a, sigma=0.5, truncate=3.5)
    f2 = ndimage.gaussian_filter(a, sigma=0.5, radius=2)
    xp_assert_equal(f1, f2)

    # Test gaussian_filter when sigma is a sequence.
    a = np.zeros((50, 50))
    a[25, 25] = 1
    a = xp.asarray(a)
    f1 = ndimage.gaussian_filter(a, sigma=[0.5, 2.5], truncate=3.5)
    f2 = ndimage.gaussian_filter(a, sigma=[0.5, 2.5], radius=[2, 9])
    xp_assert_equal(f1, f2)

