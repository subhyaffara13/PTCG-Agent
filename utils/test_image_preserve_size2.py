
def test_image_preserve_size2():
    n = 7
    data = np.identity(n, float)

    fig = plt.figure(figsize=(n, n), frameon=False)
    ax = fig.add_axes((0.0, 0.0, 1.0, 1.0))
    ax.set_axis_off()
    ax.imshow(data, interpolation='nearest', origin='lower', aspect='auto')
    buff = io.BytesIO()
    fig.savefig(buff, dpi=1)

    buff.seek(0)
    img = plt.imread(buff)

    assert img.shape == (7, 7, 4)

    assert_array_equal(np.asarray(img[:, :, 0], bool),
                       np.identity(n, bool)[::-1])

