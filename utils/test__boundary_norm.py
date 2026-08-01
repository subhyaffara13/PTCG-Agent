
def test_BoundaryNorm():
    """
    GitHub issue #1258: interpolation was failing with numpy
    1.7 pre-release.
    """

    boundaries = [0, 1.1, 2.2]
    vals = [-1, 0, 1, 2, 2.2, 4]

    # Without interpolation
    expected = [-1, 0, 0, 1, 2, 2]
    ncolors = len(boundaries) - 1
    bn = mcolors.BoundaryNorm(boundaries, ncolors)
    assert_array_equal(bn(vals), expected)

    # ncolors != len(boundaries) - 1 triggers interpolation
    expected = [-1, 0, 0, 2, 3, 3]
    ncolors = len(boundaries)
    bn = mcolors.BoundaryNorm(boundaries, ncolors)
    assert_array_equal(bn(vals), expected)

    # with a single region and interpolation
    expected = [-1, 1, 1, 1, 3, 3]
    bn = mcolors.BoundaryNorm([0, 2.2], ncolors)
    assert_array_equal(bn(vals), expected)

    # more boundaries for a third color
    boundaries = [0, 1, 2, 3]
    vals = [-1, 0.1, 1.1, 2.2, 4]
    ncolors = 5
    expected = [-1, 0, 2, 4, 5]
    bn = mcolors.BoundaryNorm(boundaries, ncolors)
    assert_array_equal(bn(vals), expected)

    # a scalar as input should not trigger an error and should return a scalar
    boundaries = [0, 1, 2]
    vals = [-1, 0.1, 1.1, 2.2]
    bn = mcolors.BoundaryNorm(boundaries, 2)
    expected = [-1, 0, 1, 2]
    for v, ex in zip(vals, expected):
        ret = bn(v)
        assert isinstance(ret, int)
        assert_array_equal(ret, ex)
        assert_array_equal(bn([v]), ex)

    # same with interp
    bn = mcolors.BoundaryNorm(boundaries, 3)
    expected = [-1, 0, 2, 3]
    for v, ex in zip(vals, expected):
        ret = bn(v)
        assert isinstance(ret, int)
        assert_array_equal(ret, ex)
        assert_array_equal(bn([v]), ex)

    # Clipping
    bn = mcolors.BoundaryNorm(boundaries, 3, clip=True)
    expected = [0, 0, 2, 2]
    for v, ex in zip(vals, expected):
        ret = bn(v)
        assert isinstance(ret, int)
        assert_array_equal(ret, ex)
        assert_array_equal(bn([v]), ex)

    # Masked arrays
    boundaries = [0, 1.1, 2.2]
    vals = np.ma.masked_invalid([-1., np.nan, 0, 1.4, 9])

    # Without interpolation
    ncolors = len(boundaries) - 1
    bn = mcolors.BoundaryNorm(boundaries, ncolors)
    expected = np.ma.masked_array([-1, -99, 0, 1, 2], mask=[0, 1, 0, 0, 0])
    assert_array_equal(bn(vals), expected)

    # With interpolation
    bn = mcolors.BoundaryNorm(boundaries, len(boundaries))
    expected = np.ma.masked_array([-1, -99, 0, 2, 3], mask=[0, 1, 0, 0, 0])
    assert_array_equal(bn(vals), expected)

    # Non-trivial masked arrays
    vals = np.ma.masked_invalid([np.inf, np.nan])
    assert np.all(bn(vals).mask)
    vals = np.ma.masked_invalid([np.inf])
    assert np.all(bn(vals).mask)

    # Incompatible extend and clip
    with pytest.raises(ValueError, match="not compatible"):
        mcolors.BoundaryNorm(np.arange(4), 5, extend='both', clip=True)

    # Too small ncolors argument
    with pytest.raises(ValueError, match="ncolors must equal or exceed"):
        mcolors.BoundaryNorm(np.arange(4), 2)

    with pytest.raises(ValueError, match="ncolors must equal or exceed"):
        mcolors.BoundaryNorm(np.arange(4), 3, extend='min')

    with pytest.raises(ValueError, match="ncolors must equal or exceed"):
        mcolors.BoundaryNorm(np.arange(4), 4, extend='both')

    # Testing extend keyword, with interpolation (large cmap)
    bounds = [1, 2, 3]
    cmap = mpl.colormaps['viridis']
    mynorm = mcolors.BoundaryNorm(bounds, cmap.N, extend='both')
    refnorm = mcolors.BoundaryNorm([0] + bounds + [4], cmap.N)
    x = np.random.randn(100) * 10 + 2
    ref = refnorm(x)
    ref[ref == 0] = -1
    ref[ref == cmap.N - 1] = cmap.N
    assert_array_equal(mynorm(x), ref)

    # Without interpolation
    cmref = mcolors.ListedColormap(['blue', 'red'], under='white', over='black')
    cmshould = mcolors.ListedColormap(['white', 'blue', 'red', 'black'])

    assert mcolors.same_color(cmref.get_over(), 'black')
    assert mcolors.same_color(cmref.get_under(), 'white')

    refnorm = mcolors.BoundaryNorm(bounds, cmref.N)
    mynorm = mcolors.BoundaryNorm(bounds, cmshould.N, extend='both')
    assert mynorm.vmin == refnorm.vmin
    assert mynorm.vmax == refnorm.vmax

    assert mynorm(bounds[0] - 0.1) == -1  # under
    assert mynorm(bounds[0] + 0.1) == 1   # first bin -> second color
    assert mynorm(bounds[-1] - 0.1) == cmshould.N - 2  # next-to-last color
    assert mynorm(bounds[-1] + 0.1) == cmshould.N  # over

    x = [-1, 1.2, 2.3, 9.6]
    assert_array_equal(cmshould(mynorm(x)), cmshould([0, 1, 2, 3]))
    x = np.random.randn(100) * 10 + 2
    assert_array_equal(cmshould(mynorm(x)), cmref(refnorm(x)))

    # Just min
    cmref = mcolors.ListedColormap(['blue', 'red'], under='white')
    cmshould = mcolors.ListedColormap(['white', 'blue', 'red'])

    assert mcolors.same_color(cmref.get_under(), 'white')

    assert cmref.N == 2
    assert cmshould.N == 3
    refnorm = mcolors.BoundaryNorm(bounds, cmref.N)
    mynorm = mcolors.BoundaryNorm(bounds, cmshould.N, extend='min')
    assert mynorm.vmin == refnorm.vmin
    assert mynorm.vmax == refnorm.vmax
    x = [-1, 1.2, 2.3]
    assert_array_equal(cmshould(mynorm(x)), cmshould([0, 1, 2]))
    x = np.random.randn(100) * 10 + 2
    assert_array_equal(cmshould(mynorm(x)), cmref(refnorm(x)))

    # Just max
    cmref = mcolors.ListedColormap(['blue', 'red'], over='black')
    cmshould = mcolors.ListedColormap(['blue', 'red', 'black'])

    assert mcolors.same_color(cmref.get_over(), 'black')

    assert cmref.N == 2
    assert cmshould.N == 3
    refnorm = mcolors.BoundaryNorm(bounds, cmref.N)
    mynorm = mcolors.BoundaryNorm(bounds, cmshould.N, extend='max')
    assert mynorm.vmin == refnorm.vmin
    assert mynorm.vmax == refnorm.vmax
    x = [1.2, 2.3, 4]
    assert_array_equal(cmshould(mynorm(x)), cmshould([0, 1, 2]))
    x = np.random.randn(100) * 10 + 2
    assert_array_equal(cmshould(mynorm(x)), cmref(refnorm(x)))

