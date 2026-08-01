
def test_clipping_with_nans():
    x = np.linspace(0, 3.14 * 2, 3000)
    y = np.sin(x)
    x[::100] = np.nan

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_ylim(-0.25, 0.25)

