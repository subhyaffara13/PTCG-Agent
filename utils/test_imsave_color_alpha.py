
def test_imsave_color_alpha():
    # Test that imsave accept arrays with ndim=3 where the third dimension is
    # color and alpha without raising any exceptions, and that the data is
    # acceptably preserved through a save/read roundtrip.
    np.random.seed(1)

    for origin in ['lower', 'upper']:
        data = np.random.rand(16, 16, 4)
        buff = io.BytesIO()
        plt.imsave(buff, data, origin=origin, format="png")

        buff.seek(0)
        arr_buf = plt.imread(buff)

        # Recreate the float -> uint8 conversion of the data
        # We can only expect to be the same with 8 bits of precision,
        # since that's what the PNG file used.
        data = (255*data).astype('uint8')
        if origin == 'lower':
            data = data[::-1]
        arr_buf = (255*arr_buf).astype('uint8')

        assert_array_equal(data, arr_buf)

