
def test_bar_label_location_horizontal_xyinverted():
    ax = plt.gca()
    ax.invert_xaxis()
    ax.invert_yaxis()
    ys, widths = [1, 2], [3, -4]
    rects = ax.barh(ys, widths)
    labels = ax.bar_label(rects)
    assert labels[0].xy == (widths[0], ys[0])
    assert labels[0].get_horizontalalignment() == 'right'
    assert labels[0].get_verticalalignment() == 'center'
    assert labels[1].xy == (widths[1], ys[1])
    assert labels[1].get_horizontalalignment() == 'left'
    assert labels[1].get_verticalalignment() == 'center'

