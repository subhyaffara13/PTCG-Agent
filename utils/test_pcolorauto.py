
def test_pcolorauto(fig_test, fig_ref, snap):
    ax = fig_test.subplots()
    x = np.arange(0, 10)
    y = np.arange(0, 4)
    np.random.seed(19680801)
    Z = np.random.randn(3, 9)
    # this is the same as flat; note that auto is default
    ax.pcolormesh(x, y, Z, snap=snap)

    ax = fig_ref.subplots()
    # specify the centers
    x2 = x[:-1] + np.diff(x) / 2
    y2 = y[:-1] + np.diff(y) / 2
    # this is same as nearest:
    ax.pcolormesh(x2, y2, Z, snap=snap)

