
def test_bbox_image_inverted():
    # This is just used to produce an image to feed to BboxImage
    image = np.arange(100).reshape((10, 10))

    fig, ax = plt.subplots()
    bbox_im = BboxImage(
        TransformedBbox(Bbox([[100, 100], [0, 0]]), ax.transData),
        interpolation='nearest')
    bbox_im.set_data(image)
    bbox_im.set_clip_on(False)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.add_artist(bbox_im)

    image = np.identity(10)

    bbox_im = BboxImage(TransformedBbox(Bbox([[0.1, 0.2], [0.3, 0.25]]),
                                        ax.get_figure().transFigure),
                        interpolation='nearest')
    bbox_im.set_data(image)
    bbox_im.set_clip_on(False)
    ax.add_artist(bbox_im)

