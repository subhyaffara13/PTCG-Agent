
def test_multivar_cmap_call():
    cmap = mpl.multivar_colormaps['2VarAddA']
    assert_array_equal(cmap((0.0, 0.0)), (0, 0, 0, 1))
    assert_array_equal(cmap((1.0, 1.0)), (1, 1, 1, 1))
    assert_allclose(cmap((0.0, 0.0), alpha=0.1), (0, 0, 0, 0.1), atol=0.1)

    cmap = mpl.multivar_colormaps['2VarSubA']
    assert_array_equal(cmap((0.0, 0.0)), (1, 1, 1, 1))
    assert_allclose(cmap((1.0, 1.0)), (0, 0, 0, 1), atol=0.1)

    # check outside and bad
    cs = cmap([(0., 0., 0., 1.2, np.nan), (0., 1.2, np.nan, 0., 0., )])
    assert_allclose(cs, [[1., 1., 1., 1.],
                         [0.801, 0.426, 0.119, 1.],
                         [0., 0., 0., 0.],
                         [0.199, 0.574, 0.881, 1.],
                         [0., 0., 0., 0.]])

    assert_array_equal(cmap((0.0, 0.0), bytes=True), (255, 255, 255, 255))

    with pytest.raises(ValueError, match="alpha is array-like but its shape"):
        cs = cmap([(0, 5, 9), (0, 0, 0)], alpha=(0.5, 0.3))

    with pytest.raises(ValueError, match="For the selected colormap the data"):
        cs = cmap([(0, 5, 9), (0, 0, 0), (0, 0, 0)])

    with pytest.raises(ValueError, match="clip cannot be false"):
        cs = cmap([(0, 5, 9), (0, 0, 0)], bytes=True, clip=False)
    # Tests calling a multivariate colormap with integer values
    cmap = mpl.multivar_colormaps['2VarSubA']

    # call only integers
    cs = cmap([(0, 50, 100, 0, 0, 300), (0, 0, 0, 50, 100, 300)])
    res = np.array([[1, 1, 1, 1],
                     [0.85176471, 0.91029412, 0.96023529, 1],
                     [0.70452941, 0.82764706, 0.93358824, 1],
                     [0.94358824, 0.88505882, 0.83511765, 1],
                     [0.89729412, 0.77417647, 0.66823529, 1],
                     [0, 0, 0, 1]])
    assert_allclose(cs,  res, atol=0.01)

    # call only integers, wrong byte order
    swapped_dt = np.dtype(int).newbyteorder()
    cs = cmap([np.array([0, 50, 100, 0, 0, 300], dtype=swapped_dt),
               np.array([0, 0, 0, 50, 100, 300], dtype=swapped_dt)])
    assert_allclose(cs,  res, atol=0.01)

    # call mix floats integers
    # check calling with bytes = True
    cs = cmap([(0, 50, 100, 0, 0, 300), (0, 0, 0, 50, 100, 300)], bytes=True)
    res = np.array([[255, 255, 255, 255],
                     [217, 232, 244, 255],
                     [179, 211, 238, 255],
                     [240, 225, 212, 255],
                     [228, 197, 170, 255],
                     [0,   0,   0, 255]])
    assert_allclose(cs,  res, atol=0.01)

    cs = cmap([(0, 50, 100, 0, 0, 300), (0, 0, 0, 50, 100, 300)], alpha=0.5)
    res = np.array([[1, 1, 1, 0.5],
                     [0.85176471, 0.91029412, 0.96023529, 0.5],
                     [0.70452941, 0.82764706, 0.93358824, 0.5],
                     [0.94358824, 0.88505882, 0.83511765, 0.5],
                     [0.89729412, 0.77417647, 0.66823529, 0.5],
                     [0, 0, 0, 0.5]])
    assert_allclose(cs,  res, atol=0.01)
    # call with tuple
    assert_allclose(cmap((100, 120), bytes=True, alpha=0.5),
                    [149, 142, 136, 127], atol=0.01)

    # alpha and bytes
    cs = cmap([(0, 5, 9, 0, 0, 10), (0, 0, 0, 5, 11, 12)], bytes=True, alpha=0.5)
    res = np.array([[0, 0, 255, 127],
                    [141, 0, 255, 127],
                    [255, 0, 255, 127],
                    [0, 115, 255, 127],
                    [0, 255, 255, 127],
                    [255, 255, 255, 127]])

    # bad alpha shape
    with pytest.raises(ValueError, match="alpha is array-like but its shape"):
        cs = cmap([(0, 5, 9), (0, 0, 0)], bytes=True, alpha=(0.5, 0.3))

    cmap = cmap.with_extremes(bad=(1, 1, 1, 1))
    cs = cmap([(0., 1.1, np.nan), (0., 1.2, 1.)])
    res = np.array([[1., 1., 1., 1.],
                   [0., 0., 0., 1.],
                   [1., 1., 1., 1.]])
    assert_allclose(cs,  res, atol=0.01)

    # call outside with tuple
    assert_allclose(cmap((300, 300), bytes=True, alpha=0.5),
                    [0, 0, 0, 127], atol=0.01)
    with pytest.raises(ValueError,
                       match="For the selected colormap the data must have"):
        cs = cmap((0, 5, 9))

    # test over/under
    cmap = mpl.multivar_colormaps['2VarAddA']
    with pytest.raises(ValueError, match='i.e. be of length 2'):
        cmap.with_extremes(over=0)
    with pytest.raises(ValueError, match='i.e. be of length 2'):
        cmap.with_extremes(under=0)

    cmap = cmap.with_extremes(under=[(0, 0, 0, 0)]*2)
    assert_allclose((0, 0, 0, 0), cmap((-1., 0)), atol=1e-2)
    cmap = cmap.with_extremes(over=[(0, 0, 0, 0)]*2)
    assert_allclose((0, 0, 0, 0), cmap((2., 0)), atol=1e-2)

