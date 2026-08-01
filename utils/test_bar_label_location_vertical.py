
def test_bar_label_location_vertical():
    ax = plt.gca()
    xs, heights = [1, 2], [3, -4]
    rects = ax.bar(xs, heights)
    labels = ax.bar_label(rects)
    assert labels[0].xy == (xs[0], heights[0])
    assert labels[0].get_horizontalalignment() == 'center'
    assert labels[0].get_verticalalignment() == 'bottom'
    assert labels[1].xy == (xs[1], heights[1])
    assert labels[1].get_horizontalalignment() == 'center'
    assert labels[1].get_verticalalignment() == 'top'

