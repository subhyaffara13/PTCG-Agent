
def test_para_equal_perp():
    x = np.array([0, 1, 2, 1, 0, -1, 0, 1] + [1] * 128)
    y = np.array([1, 1, 2, 1, 0, -1, 0, 0] + [0] * 128)

    fig, ax = plt.subplots()
    ax.plot(x + 1, y + 1)
    ax.plot(x + 1, y + 1, 'ro')

