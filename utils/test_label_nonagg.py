
def test_label_nonagg():
    # This should not crash even if the canvas doesn't have a get_renderer().
    plt.clabel(plt.contour([[1, 2], [3, 4]]))

