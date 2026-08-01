
def test_unclipped():
    fig, ax = plt.subplots()
    ax.set_axis_off()
    im = ax.imshow([[0, 0], [0, 0]], aspect="auto", extent=(-10, 10, -10, 10),
                   cmap='gray', clip_on=False)
    ax.set(xlim=(0, 1), ylim=(0, 1))
    fig.canvas.draw()
    # The unclipped image should fill the *entire* figure and be black.
    # Ignore alpha for this comparison.
    assert (np.array(fig.canvas.buffer_rgba())[..., :3] == 0).all()

