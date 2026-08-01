
def test_colorbar_autotickslog():
    # Test new autotick modes...
    with rc_context({'_internal.classic_mode': False}):
        fig, ax = plt.subplots(2, 1)
        x = np.arange(-3.0, 4.001)
        y = np.arange(-4.0, 3.001)
        X, Y = np.meshgrid(x, y)
        Z = X * Y
        Z = Z[:-1, :-1]
        pcm = ax[0].pcolormesh(X, Y, 10**Z, norm=LogNorm())
        cbar = fig.colorbar(pcm, ax=ax[0], extend='both',
                            orientation='vertical')

        pcm = ax[1].pcolormesh(X, Y, 10**Z, norm=LogNorm())
        cbar2 = fig.colorbar(pcm, ax=ax[1], extend='both',
                             orientation='vertical', shrink=0.4)

        fig.draw_without_rendering()
        # note only -12 to +12 are visible
        np.testing.assert_equal(np.log10(cbar.ax.yaxis.get_ticklocs()),
                                [-18, -12, -6, 0, +6, +12, +18])
        np.testing.assert_equal(np.log10(cbar2.ax.yaxis.get_ticklocs()),
                                [-36, -12, 12, +36])

