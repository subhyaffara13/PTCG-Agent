
def test_diamond():
    x = np.array([0.0, 1.0, 0.0, -1.0, 0.0])
    y = np.array([1.0, 0.0, -1.0, 0.0, 1.0])

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlim(-0.6, 0.6)
    ax.set_ylim(-0.6, 0.6)

