
def test_pcolormesh_nearest_noargs(fig_test, fig_ref):
    x = np.arange(4)
    y = np.arange(7)
    X, Y = np.meshgrid(x, y)
    C = X + Y

    ax = fig_test.subplots()
    ax.pcolormesh(C, shading="nearest")

    ax = fig_ref.subplots()
    ax.pcolormesh(x, y, C, shading="nearest")

