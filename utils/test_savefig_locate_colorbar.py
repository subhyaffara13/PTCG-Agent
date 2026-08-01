
def test_savefig_locate_colorbar():
    fig, ax = plt.subplots()
    pc = ax.pcolormesh(np.random.randn(2, 2))
    cbar = fig.colorbar(pc, aspect=40)
    fig.savefig(io.BytesIO(), bbox_inches=mpl.transforms.Bbox([[0, 0], [4, 4]]))

    # Check that an aspect ratio has been applied.
    assert (cbar.ax.get_position(original=True).bounds !=
            cbar.ax.get_position(original=False).bounds)

