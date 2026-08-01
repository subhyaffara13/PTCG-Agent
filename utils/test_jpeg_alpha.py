
def test_jpeg_alpha():
    plt.figure(figsize=(1, 1), dpi=300)
    # Create an image that is all black, with a gradient from 0-1 in
    # the alpha channel from left to right.
    im = np.zeros((300, 300, 4), dtype=float)
    im[..., 3] = np.linspace(0.0, 1.0, 300)

    plt.figimage(im)

    buff = io.BytesIO()
    plt.savefig(buff, facecolor="red", format='jpg', dpi=300)

    buff.seek(0)
    image = Image.open(buff)

    # If this fails, there will be only one color (all black). If this
    # is working, we should have all 256 shades of grey represented.
    num_colors = len(image.getcolors(256))
    assert 175 <= num_colors <= 230
    # The fully transparent part should be red.
    corner_pixel = image.getpixel((0, 0))
    assert corner_pixel == (254, 0, 0)

