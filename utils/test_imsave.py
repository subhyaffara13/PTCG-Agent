
def test_imsave(fmt):
    has_alpha = fmt not in ["jpg", "jpeg"]

    # The goal here is that the user can specify an output logical DPI
    # for the image, but this will not actually add any extra pixels
    # to the image, it will merely be used for metadata purposes.

    # So we do the traditional case (dpi == 1), and the new case (dpi
    # == 100) and read the resulting PNG files back in and make sure
    # the data is 100% identical.
    np.random.seed(1)
    # The height of 1856 pixels was selected because going through creating an
    # actual dpi=100 figure to save the image to a Pillow-provided format would
    # cause a rounding error resulting in a final image of shape 1855.
    data = np.random.rand(1856, 2)

    buff_dpi1 = io.BytesIO()
    plt.imsave(buff_dpi1, data, format=fmt, dpi=1)

    buff_dpi100 = io.BytesIO()
    plt.imsave(buff_dpi100, data, format=fmt, dpi=100)

    buff_dpi1.seek(0)
    arr_dpi1 = plt.imread(buff_dpi1, format=fmt)

    buff_dpi100.seek(0)
    arr_dpi100 = plt.imread(buff_dpi100, format=fmt)

    assert arr_dpi1.shape == (1856, 2, 3 + has_alpha)
    assert arr_dpi100.shape == (1856, 2, 3 + has_alpha)

    assert_array_equal(arr_dpi1, arr_dpi100)

