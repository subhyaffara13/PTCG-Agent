
def test_image_preserve_size():
    buff = io.BytesIO()

    im = np.zeros((481, 321))
    plt.imsave(buff, im, format="png")

    buff.seek(0)
    img = plt.imread(buff)

    assert img.shape[:2] == im.shape

