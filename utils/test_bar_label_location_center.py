
def test_bar_label_location_center():
    ax = plt.gca()
    ys, widths = [1, 2], [3, -4]
    rects = ax.barh(ys, widths)
    labels = ax.bar_label(rects, label_type='center')
    assert labels[0].xy == (0.5, 0.5)
    assert labels[0].get_horizontalalignment() == 'center'
    assert labels[0].get_verticalalignment() == 'center'
    assert labels[1].xy == (0.5, 0.5)
    assert labels[1].get_horizontalalignment() == 'center'
    assert labels[1].get_verticalalignment() == 'center'

