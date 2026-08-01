
def test_contour_aliases(fig_test, fig_ref):
    data = np.arange(100).reshape((10, 10)) ** 2
    fig_test.add_subplot().contour(data, linestyle=":")
    fig_ref.add_subplot().contour(data, linestyles="dotted")

