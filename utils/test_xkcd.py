
def test_xkcd():
    np.random.seed(0)

    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)

    with plt.xkcd():
        fig, ax = plt.subplots()
        ax.plot(x, y)

