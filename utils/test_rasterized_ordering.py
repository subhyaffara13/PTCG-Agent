
def test_rasterized_ordering(fig_test, fig_ref):
    t = np.arange(0, 100) * (2.3)
    x = np.cos(t)
    y = np.sin(t)

    ax_ref = fig_ref.subplots()
    ax_ref.set_xlim(0, 3)
    ax_ref.set_ylim(-1.1, 1.1)
    ax_ref.plot(x, y, "-", c="r", lw=10, rasterized=True)
    ax_ref.plot(x+1, y, "-", c="b", lw=10, rasterized=False)
    ax_ref.plot(x+2, y, "-", c="g", lw=10, rasterized=True)
    ax_ref.plot(x+3, y, "-", c="m", lw=10, rasterized=True)

    ax_test = fig_test.subplots()
    ax_test.set_xlim(0, 3)
    ax_test.set_ylim(-1.1, 1.1)
    ax_test.plot(x, y, "-", c="r", lw=10, rasterized=True, zorder=1.1)
    ax_test.plot(x+2, y, "-", c="g", lw=10, rasterized=True, zorder=1.3)
    ax_test.plot(x+3, y, "-", c="m", lw=10, rasterized=True, zorder=1.4)
    ax_test.plot(x+1, y, "-", c="b", lw=10, rasterized=False, zorder=1.2)

