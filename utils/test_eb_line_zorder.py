
def test_eb_line_zorder():
    x = list(range(10))

    # First illustrate basic pyplot interface, using defaults where possible.
    fig = plt.figure()
    ax = fig.gca()
    ax.plot(x, lw=10, zorder=5)
    ax.axhline(1, color='red', lw=10, zorder=1)
    ax.axhline(5, color='green', lw=10, zorder=10)
    ax.axvline(7, color='m', lw=10, zorder=7)
    ax.axvline(2, color='k', lw=10, zorder=3)

    ax.set_title("axvline and axhline zorder test")

    # Now switch to a more OO interface to exercise more features.
    fig = plt.figure()
    ax = fig.gca()
    x = list(range(10))
    y = np.zeros(10)
    yerr = list(range(10))
    ax.errorbar(x, y, yerr=yerr, zorder=5, lw=5, color='r')
    for j in range(10):
        ax.axhline(j, lw=5, color='k', zorder=j)
        ax.axhline(-j, lw=5, color='k', zorder=j)

    ax.set_title("errorbar zorder test")

