
def test_image_edges():
    fig = plt.figure(figsize=[1, 1])
    ax = fig.add_axes((0, 0, 1, 1), frameon=False)

    data = np.tile(np.arange(12), 15).reshape(20, 9)

    im = ax.imshow(data, origin='upper', extent=[-10, 10, -10, 10],
                   interpolation='none', cmap='gray')

    x = y = 2
    ax.set_xlim(-x, x)
    ax.set_ylim(-y, y)

    ax.set_xticks([])
    ax.set_yticks([])

    buf = io.BytesIO()
    fig.savefig(buf, facecolor=(0, 1, 0))

    buf.seek(0)

    im = plt.imread(buf)
    r, g, b, a = sum(im[:, 0])
    r, g, b, a = sum(im[:, -1])

    assert g != 100, 'Expected a non-green edge - but sadly, it was.'

