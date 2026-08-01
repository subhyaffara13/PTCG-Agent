
def test_jpeg_2d():
    # smoke test that mode-L pillow images work.
    imd = np.ones((10, 10), dtype='uint8')
    for i in range(10):
        imd[i, :] = np.linspace(0.0, 1.0, 10) * 255
    im = Image.new('L', (10, 10))
    im.putdata(imd.flatten())
    fig, ax = plt.subplots()
    ax.imshow(im)

