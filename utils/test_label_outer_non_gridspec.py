
def test_label_outer_non_gridspec():
    ax = plt.axes((0, 0, 1, 1))
    ax.label_outer()  # Does nothing.
    check_ticklabel_visible([ax], [True], [True])

