
def test_tight_pcolorfast():
    fig, ax = plt.subplots()
    ax.pcolorfast(np.arange(4).reshape((2, 2)))
    ax.set(ylim=(0, .1))
    buf = BytesIO()
    fig.savefig(buf, bbox_inches="tight")
    buf.seek(0)
    height, width, _ = plt.imread(buf).shape
    # Previously, the bbox would include the area of the image clipped out by
    # the axes, resulting in a very tall image given the y limits of (0, 0.1).
    assert width > height

