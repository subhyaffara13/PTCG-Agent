
def test_culling(fig_test, fig_ref):
    xmins = (-100, -50)
    for fig, xmin in zip((fig_test, fig_ref), xmins):
        ax = fig.add_subplot(projection='3d')
        n = abs(xmin) + 1
        xs = np.linspace(0, xmin, n)
        ys = np.ones(n)
        zs = np.zeros(n)
        ax.plot(xs, ys, zs, 'k')

        ax.set(xlim=(-5, 5), ylim=(-5, 5), zlim=(-5, 5))
        ax.view_init(5, 180, 0)

