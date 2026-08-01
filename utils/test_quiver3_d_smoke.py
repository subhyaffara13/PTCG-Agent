
def test_quiver3D_smoke(fig_test, fig_ref):
    pivot = "middle"
    # Make the grid
    x, y, z = np.meshgrid(
        np.arange(-0.8, 1, 0.2),
        np.arange(-0.8, 1, 0.2),
        np.arange(-0.8, 1, 0.8)
    )
    u = v = w = np.ones_like(x)

    for fig, length in zip((fig_ref, fig_test), (1, 1.0)):
        ax = fig.add_subplot(projection="3d")
        ax.quiver(x, y, z, u, v, w, length=length, pivot=pivot)

