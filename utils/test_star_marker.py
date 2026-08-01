
def test_star_marker():
    # We don't really have a strict equivalent to this marker, so we'll just do
    # a smoke test.
    size = 20**2

    fig, ax = plt.subplots()
    ax.scatter([0], [0], marker=(5, 1), s=size)
    ax.scatter([1], [1], marker=(5, 1, 0), s=size)
    ax.set(xlim=(-0.5, 0.5), ylim=(-0.5, 1.5))

