
def test_inset_polar():
    _, ax = plt.subplots()
    axins = ax.inset_axes([0.5, 0.1, 0.45, 0.45], polar=True)
    assert isinstance(axins, PolarAxes)

    r = np.arange(0, 2, 0.01)
    theta = 2 * np.pi * r

    ax.plot(theta, r)
    axins.plot(theta, r)

