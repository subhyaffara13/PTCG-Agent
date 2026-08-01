
def test_colorbar_autoticks():
    # Test new autotick modes. Needs to be classic because
    # non-classic doesn't go this route.
    with rc_context({'_internal.classic_mode': False}):
        fig, ax = plt.subplots(2, 1)
        x = np.arange(-3.0, 4.001)
        y = np.arange(-4.0, 3.001)
        X, Y = np.meshgrid(x, y)
        Z = X * Y
        Z = Z[:-1, :-1]
        pcm = ax[0].pcolormesh(X, Y, Z)
        cbar = fig.colorbar(pcm, ax=ax[0], extend='both',
                            orientation='vertical')

        pcm = ax[1].pcolormesh(X, Y, Z)
        cbar2 = fig.colorbar(pcm, ax=ax[1], extend='both',
                             orientation='vertical', shrink=0.4)
        # note only -10 to 10 are visible,
        np.testing.assert_almost_equal(cbar.ax.yaxis.get_ticklocs(),
                                       np.arange(-15, 16, 5))
        # note only -10 to 10 are visible
        np.testing.assert_almost_equal(cbar2.ax.yaxis.get_ticklocs(),
                                       np.arange(-20, 21, 10))

