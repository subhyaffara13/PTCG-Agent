
def test_linestyle_single_dashes():
    plt.scatter([0, 1, 2], [0, 1, 2], linestyle=(0., [2., 2.]))
    plt.draw()

