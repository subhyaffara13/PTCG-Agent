
def test_constrained_layout20():
    """Smoke test cl does not mess up added Axes"""
    gx = np.linspace(-5, 5, 4)
    img = np.hypot(gx, gx[:, None])

    fig = plt.figure()
    ax = fig.add_axes((0, 0, 1, 1))
    mesh = ax.pcolormesh(gx, gx, img[:-1, :-1])
    fig.colorbar(mesh)

