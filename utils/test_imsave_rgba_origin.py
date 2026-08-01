
def test_imsave_rgba_origin(origin):
    # test that imsave always passes c-contiguous arrays down to pillow
    buf = io.BytesIO()
    result = np.zeros((10, 10, 4), dtype='uint8')
    mimage.imsave(buf, arr=result, format="png", origin=origin)

