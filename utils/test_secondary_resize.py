
def test_secondary_resize():
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(np.arange(2, 11), np.arange(2, 11))

    def invert(x):
        with np.errstate(divide='ignore'):
            return 1 / x

    ax.secondary_xaxis('top', functions=(invert, invert))
    fig.canvas.draw()
    fig.set_size_inches((7, 4))
    assert_allclose(ax.get_position().extents, [0.125, 0.1, 0.9, 0.9])

