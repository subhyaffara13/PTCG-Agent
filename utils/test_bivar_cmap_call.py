
def test_bivar_cmap_call():
    """
    Tests calling a bivariate colormap with integer values
    """
    im = np.ones((10, 12, 4))
    im[:, :, 0] = np.linspace(0, 1, 10)[:, np.newaxis]
    im[:, :, 1] = np.linspace(0, 1, 12)[np.newaxis, :]
    cmap = mpl.colors.BivarColormapFromImage(im)

    # call only integers
    cs = cmap([(0, 5, 9, 0, 0, 10), (0, 0, 0, 5, 11, 12)])
    res = np.array([[0, 0, 1, 1],
                   [0.556, 0, 1, 1],
                   [1, 0, 1, 1],
                   [0, 0.454, 1, 1],
                   [0, 1, 1, 1],
                   [1, 1, 1, 1]])
    assert_allclose(cs,  res, atol=0.01)
    # call only integers, wrong byte order
    swapped_dt = np.dtype(int).newbyteorder()
    cs = cmap([np.array([0, 5, 9, 0, 0, 10], dtype=swapped_dt),
               np.array([0, 0, 0, 5, 11, 12], dtype=swapped_dt)])
    assert_allclose(cs,  res, atol=0.01)

    # call mix floats integers
    cmap = cmap.with_extremes(outside=(1, 0, 0, 0))
    cs = cmap([(0.5, 0), (0, 3)])
    res = np.array([[0.555, 0, 1, 1],
                    [0, 0.2727, 1, 1]])
    assert_allclose(cs,  res, atol=0.01)

    # check calling with bytes = True
    cs = cmap([(0, 5, 9, 0, 0, 10), (0, 0, 0, 5, 11, 12)], bytes=True)
    res = np.array([[0, 0, 255, 255],
                    [141, 0, 255, 255],
                    [255, 0, 255, 255],
                    [0, 115, 255, 255],
                    [0, 255, 255, 255],
                    [255, 255, 255, 255]])
    assert_allclose(cs,  res, atol=0.01)

    # test alpha
    cs = cmap([(0, 5, 9, 0, 0, 10), (0, 0, 0, 5, 11, 12)], alpha=0.5)
    res = np.array([[0, 0, 1, 0.5],
                    [0.556, 0, 1, 0.5],
                    [1, 0, 1, 0.5],
                    [0, 0.454, 1, 0.5],
                    [0, 1, 1, 0.5],
                    [1, 1, 1, 0.5]])
    assert_allclose(cs,  res, atol=0.01)
    # call with tuple
    assert_allclose(cmap((10, 12), bytes=True, alpha=0.5),
                    [255, 255, 255, 127], atol=0.01)

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

    # set shape to 'ignore'.
    # final point is outside colormap and should then receive
    # the 'outside' (in this case [1,0,0,0])
    # also test 'bad' (in this case [1,1,1,0])
    cmap = cmap.with_extremes(outside=(1, 0, 0, 0), bad=(1, 1, 1, 0), shape='ignore')
    cs = cmap([(0., 1.1, np.nan), (0., 1.2, 1.)])
    res = np.array([[0, 0, 1, 1],
                    [1, 0, 0, 0],
                    [1, 1, 1, 0]])
    assert_allclose(cs,  res, atol=0.01)
    # call outside with tuple
    assert_allclose(cmap((10, 12), bytes=True, alpha=0.5),
                    [255, 0, 0, 127], atol=0.01)
    # with integers
    cs = cmap([(0, 10), (0, 12)])
    res = np.array([[0, 0, 1, 1],
                    [1, 0, 0, 0]])
    assert_allclose(cs,  res, atol=0.01)

    with pytest.raises(ValueError,
                       match="For a `BivarColormap` the data must have"):
        cs = cmap((0, 5, 9))

    cmap = cmap.with_extremes(shape='circle')
    with pytest.raises(NotImplementedError,
                       match="only implemented for use with with floats"):
        cs = cmap([(0, 5, 9, 0, 0, 9), (0, 0, 0, 5, 11, 11)])

