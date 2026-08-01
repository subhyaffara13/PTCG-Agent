
def test_xkcd_marker():
    np.random.seed(0)

    x = np.linspace(0, 5, 8)
    y1 = x
    y2 = 5 - x
    y3 = 2.5 * np.ones(8)

    with plt.xkcd():
        fig, ax = plt.subplots()
        ax.plot(x, y1, '+', ms=10)
        ax.plot(x, y2, 'o', ms=10)
        ax.plot(x, y3, '^', ms=10)

