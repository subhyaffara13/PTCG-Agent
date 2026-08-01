
def test_axesimage_get_shape():
    # generate dummy image to test get_shape method
    ax = plt.gca()
    im = AxesImage(ax)
    with pytest.raises(RuntimeError, match="You must first set the image array"):
        im.get_shape()
    z = np.arange(12, dtype=float).reshape((4, 3))
    im.set_data(z)
    assert im.get_shape() == (4, 3)
    assert im.get_size() == im.get_shape()

