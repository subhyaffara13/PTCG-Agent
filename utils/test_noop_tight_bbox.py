
def test_noop_tight_bbox():
    from PIL import Image
    x_size, y_size = (10, 7)
    dpi = 100
    # make the figure just the right size up front
    fig = plt.figure(frameon=False, dpi=dpi, figsize=(x_size/dpi, y_size/dpi))
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_axis_off()
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    data = np.arange(x_size * y_size).reshape(y_size, x_size)
    ax.imshow(data, rasterized=True)

    # When a rasterized Artist is included, a mixed-mode renderer does
    # additional bbox adjustment. It should also be a no-op, and not affect the
    # next save.
    fig.savefig(BytesIO(), bbox_inches='tight', pad_inches=0, format='pdf')

    out = BytesIO()
    fig.savefig(out, bbox_inches='tight', pad_inches=0)
    out.seek(0)
    im = np.asarray(Image.open(out))
    assert (im[:, :, 3] == 255).all()
    assert not (im[:, :, :3] == 255).all()
    assert im.shape == (7, 10, 4)

