
def test_secondary_minorloc():
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(np.arange(2, 11), np.arange(2, 11))

    def invert(x):
        with np.errstate(divide='ignore'):
            return 1 / x

    secax = ax.secondary_xaxis('top', functions=(invert, invert))
    assert isinstance(secax._axis.get_minor_locator(),
                      mticker.NullLocator)
    secax.minorticks_on()
    assert isinstance(secax._axis.get_minor_locator(),
                      mticker.AutoMinorLocator)
    ax.set_xscale('log')
    plt.draw()
    assert isinstance(secax._axis.get_minor_locator(),
                      mticker.LogLocator)
    ax.set_xscale('linear')
    plt.draw()
    assert isinstance(secax._axis.get_minor_locator(),
                      mticker.NullLocator)

