
def test_bivar_cmap_from_image():
    """
    This tests the creation and use of a bivariate colormap
    generated from an image
    """

    data_0 = np.arange(6).reshape((2, 3))/5
    data_1 = np.arange(6).reshape((3, 2)).T/5

    # bivariate colormap from array
    cim = np.ones((10, 12, 3))
    cim[:, :, 0] = np.arange(10)[:, np.newaxis]/10
    cim[:, :, 1] = np.arange(12)[np.newaxis, :]/12

    cmap = mpl.colors.BivarColormapFromImage(cim)
    im = cmap((data_0, data_1))
    res = np.array([[[0, 0, 1, 1],
                    [0.2, 0.33333333, 1, 1],
                    [0.4, 0.75, 1, 1]],
                   [[0.6, 0.16666667, 1, 1],
                    [0.8, 0.58333333, 1, 1],
                    [0.9, 0.91666667, 1, 1]]])
    assert_allclose(im,  res, atol=0.01)

    # input as unit8
    cim = np.ones((10, 12, 3))*255
    cim[:, :, 0] = np.arange(10)[:, np.newaxis]/10*255
    cim[:, :, 1] = np.arange(12)[np.newaxis, :]/12*255

    cmap = mpl.colors.BivarColormapFromImage(cim.astype(np.uint8))
    im = cmap((data_0, data_1))
    res = np.array([[[0, 0, 1, 1],
                    [0.2, 0.33333333, 1, 1],
                    [0.4, 0.75, 1, 1]],
                   [[0.6, 0.16666667, 1, 1],
                    [0.8, 0.58333333, 1, 1],
                    [0.9, 0.91666667, 1, 1]]])
    assert_allclose(im,  res, atol=0.01)

    # bivariate colormap from array
    png_path = Path(__file__).parent / "baseline_images/pngsuite/basn2c16.png"
    cim = Image.open(png_path)
    cim = np.asarray(cim.convert('RGBA'))

    cmap = mpl.colors.BivarColormapFromImage(cim)
    im = cmap((data_0, data_1), bytes=True)
    res = np.array([[[255, 255,   0, 255],
                     [156, 206,   0, 255],
                     [49, 156,  49, 255]],
                    [[206,  99,   0, 255],
                     [99,  49, 107, 255],
                     [0,   0, 255, 255]]])
    assert_allclose(im,  res, atol=0.01)

