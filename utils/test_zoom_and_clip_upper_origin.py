
def test_zoom_and_clip_upper_origin():
    image = np.arange(100)
    image = image.reshape((10, 10))

    fig, ax = plt.subplots()
    ax.imshow(image)
    ax.set_ylim(2.0, -0.5)
    ax.set_xlim(-0.5, 2.0)

