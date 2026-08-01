
def test_exact_vmin():
    cmap = mpl.colormaps["autumn_r"].with_extremes(under="lightgrey")

    # make the image exactly 190 pixels wide
    fig = plt.figure(figsize=(1.9, 0.1), dpi=100)
    ax = fig.add_axes((0, 0, 1, 1))

    data = np.array(
        [[-1, -1, -1, 0, 0, 0, 0, 43, 79, 95, 66, 1, -1, -1, -1, 0, 0, 0, 34]],
        dtype=float,
    )

    im = ax.imshow(data, aspect="auto", cmap=cmap, vmin=0, vmax=100)
    ax.axis("off")
    fig.canvas.draw()

    # get the RGBA slice from the image
    from_image = im.make_image(fig.canvas.renderer)[0][0]
    # expand the input to be 190 long and run through norm / cmap
    direct_computation = (
        im.cmap(im.norm((data * ([[1]] * 10)).T.ravel())) * 255
    ).astype(int)

    # check than the RBGA values are the same
    assert np.all(from_image == direct_computation)

