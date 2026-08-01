
def test_gaussian_truncate(xp):
    # Test that Gaussian filters can be truncated at different widths.
    # These tests only check that the result has the expected number
    # of nonzero elements.
    arr = np.zeros((100, 100), dtype=np.float64)
    arr[50, 50] = 1
    arr = xp.asarray(arr)
    num_nonzeros_2 = _count_nonzero(ndimage.gaussian_filter(arr, 5, truncate=2) > 0)
    assert num_nonzeros_2 == 21**2

    num_nonzeros_5 = _count_nonzero(
        ndimage.gaussian_filter(arr, 5, truncate=5) > 0
    )
    assert num_nonzeros_5 == 51**2

    # Test truncate when sigma is a sequence.
    f = ndimage.gaussian_filter(arr, [0.5, 2.5], truncate=3.5)
    fpos = f > 0
    n0 = _count_nonzero(xp.any(fpos, axis=0))
    assert n0 == 19
    n1 = _count_nonzero(xp.any(fpos, axis=1))
    assert n1 == 5

    # Test gaussian_filter1d.
    x = np.zeros(51)
    x[25] = 1
    x = xp.asarray(x)
    f = ndimage.gaussian_filter1d(x, sigma=2, truncate=3.5)
    n = _count_nonzero(f > 0)
    assert n == 15

    # Test gaussian_laplace
    y = ndimage.gaussian_laplace(x, sigma=2, truncate=3.5)
    nonzero_indices = xp.nonzero(y != 0)[0]

    n = xp.max(nonzero_indices) - xp.min(nonzero_indices) + 1
    assert n == 15

    # Test gaussian_gradient_magnitude
    y = ndimage.gaussian_gradient_magnitude(x, sigma=2, truncate=3.5)
    nonzero_indices = xp.nonzero(y != 0)[0]
    n = xp.max(nonzero_indices) - xp.min(nonzero_indices) + 1
    assert n == 15

