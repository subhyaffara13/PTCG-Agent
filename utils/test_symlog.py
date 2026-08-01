
def test_symlog():
    x = np.array([0, 1, 2, 4, 6, 9, 12, 24])
    y = np.array([1000000, 500000, 100000, 100, 5, 0, 0, 0])

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_yscale('symlog')
    ax.set_xscale('linear')
    ax.set_ylim(-1, 10000000)

