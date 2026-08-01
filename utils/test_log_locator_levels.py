
def test_log_locator_levels():

    fig, ax = plt.subplots()

    N = 100
    x = np.linspace(-3.0, 3.0, N)
    y = np.linspace(-2.0, 2.0, N)

    X, Y = np.meshgrid(x, y)

    Z1 = np.exp(-X**2 - Y**2)
    Z2 = np.exp(-(X * 10)**2 - (Y * 10)**2)
    data = Z1 + 50 * Z2

    c = ax.contourf(data, locator=ticker.LogLocator())
    assert_array_almost_equal(c.levels, np.power(10.0, np.arange(-6, 3)))
    cb = fig.colorbar(c, ax=ax)
    assert_array_almost_equal(cb.ax.get_yticks(), c.levels)

