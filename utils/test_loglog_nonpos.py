
def test_loglog_nonpos():
    fig, axs = plt.subplots(3, 3)
    x = np.arange(1, 11)
    y = x**3
    y[7] = -3.
    x[4] = -10
    for (mcy, mcx), ax in zip(product(['mask', 'clip', ''], repeat=2),
                              axs.flat):
        if mcx == mcy:
            if mcx:
                ax.loglog(x, y**3, lw=2, nonpositive=mcx)
            else:
                ax.loglog(x, y**3, lw=2)
        else:
            ax.loglog(x, y**3, lw=2)
            if mcx:
                ax.set_xscale("log", nonpositive=mcx)
            if mcy:
                ax.set_yscale("log", nonpositive=mcy)
        ax.set_yticks([1e3, 1e7])  # Backcompat tick selection.

