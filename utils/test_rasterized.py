
def test_rasterized(fig_test, fig_ref):
    t = np.arange(0, 100) * (2.3)
    x = np.cos(t)
    y = np.sin(t)

    ax_ref = fig_ref.subplots()
    ax_ref.plot(x, y, "-", c="r", lw=10)
    ax_ref.plot(x+1, y, "-", c="b", lw=10)

    ax_test = fig_test.subplots()
    ax_test.plot(x, y, "-", c="r", lw=10, rasterized=True)
    ax_test.plot(x+1, y, "-", c="b", lw=10, rasterized=True)

