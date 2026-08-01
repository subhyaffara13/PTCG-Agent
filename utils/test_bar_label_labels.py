
def test_bar_label_labels():
    ax = plt.gca()
    rects = ax.bar([1, 2], [3, -4])
    labels = ax.bar_label(rects, labels=['A', 'B'])
    assert labels[0].get_text() == 'A'
    assert labels[1].get_text() == 'B'

