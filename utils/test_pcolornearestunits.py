
def test_pcolornearestunits(fig_test, fig_ref):
    ax = fig_test.subplots()
    x = [datetime.datetime.fromtimestamp(x * 3600) for x in range(10)]
    y = np.arange(0, 3)
    np.random.seed(19680801)
    Z = np.random.randn(2, 9)
    ax.pcolormesh(x, y, Z, shading='flat')

    ax = fig_ref.subplots()
    # specify the centers
    x2 = [datetime.datetime.fromtimestamp((x + 0.5) * 3600) for x in range(9)]
    y2 = y[:-1] + np.diff(y) / 2
    ax.pcolormesh(x2, y2, Z, shading='nearest')

