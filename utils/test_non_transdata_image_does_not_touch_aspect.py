
def test_non_transdata_image_does_not_touch_aspect():
    ax = plt.figure().add_subplot()
    im = np.arange(4).reshape((2, 2))
    ax.imshow(im, transform=ax.transAxes)
    assert ax.get_aspect() == "auto"
    ax.imshow(im, transform=Affine2D().scale(2) + ax.transData)
    assert ax.get_aspect() == 1
    ax.imshow(im, transform=ax.transAxes, aspect=2)
    assert ax.get_aspect() == 2

