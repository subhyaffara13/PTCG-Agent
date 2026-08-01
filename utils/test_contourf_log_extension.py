
def test_contourf_log_extension():
    # Remove this line when this test image is regenerated.
    plt.rcParams['pcolormesh.snap'] = False

    # Test that contourf with lognorm is extended correctly
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 5))
    fig.subplots_adjust(left=0.05, right=0.95)

    # make data set with large range e.g. between 1e-8 and 1e10
    data_exp = np.linspace(-7.5, 9.5, 1200)
    data = np.power(10, data_exp).reshape(30, 40)
    # make manual levels e.g. between 1e-4 and 1e-6
    levels_exp = np.arange(-4., 7.)
    levels = np.power(10., levels_exp)

    # original data
    # FIXME: Force tick locations for now for backcompat with old test
    # (log-colorbar extension is not really optimal anyways).
    c1 = ax1.contourf(data,
                      norm=LogNorm(vmin=data.min(), vmax=data.max()),
                      locator=mpl.ticker.FixedLocator(10.**np.arange(-8, 12, 2)))
    # just show data in levels
    c2 = ax2.contourf(data, levels=levels,
                      norm=LogNorm(vmin=levels.min(), vmax=levels.max()),
                      extend='neither')
    # extend data from levels
    c3 = ax3.contourf(data, levels=levels,
                      norm=LogNorm(vmin=levels.min(), vmax=levels.max()),
                      extend='both')
    cb = plt.colorbar(c1, ax=ax1)
    assert cb.ax.get_ylim() == (1e-8, 1e10)
    cb = plt.colorbar(c2, ax=ax2)
    assert_array_almost_equal_nulp(cb.ax.get_ylim(), np.array((1e-4, 1e6)))
    cb = plt.colorbar(c3, ax=ax3)

