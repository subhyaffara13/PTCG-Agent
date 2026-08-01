
def test_logscale_nonpos_values():
    np.random.seed(19680801)
    xs = np.random.normal(size=int(1e3))
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    ax1.hist(xs, range=(-5, 5), bins=10)
    ax1.set_yscale('log')
    ax2.hist(xs, range=(-5, 5), bins=10)
    ax2.set_yscale('log', nonpositive='mask')

    xdata = np.arange(0, 10, 0.01)
    ydata = np.exp(-xdata)
    edata = 0.2*(10-xdata)*np.cos(5*xdata)*np.exp(-xdata)

    ax3.fill_between(xdata, ydata - edata, ydata + edata)
    ax3.set_yscale('log')

    x = np.logspace(-1, 1)
    y = x ** 3
    yerr = x**2
    ax4.errorbar(x, y, yerr=yerr)

    ax4.set_yscale('log')
    ax4.set_xscale('log')
    ax4.set_yticks([1e-2, 1, 1e+2])  # Backcompat tick selection.

