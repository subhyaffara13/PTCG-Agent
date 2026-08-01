
def test_zooming_with_inverted_axes():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 2, 3])
    ax.axis([1, 3, 1, 3])
    inset_ax = zoomed_inset_axes(ax, zoom=2.5, loc='lower right')
    inset_ax.axis([1.1, 1.4, 1.1, 1.4])

    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 2, 3])
    ax.axis([3, 1, 3, 1])
    inset_ax = zoomed_inset_axes(ax, zoom=2.5, loc='lower right')
    inset_ax.axis([1.4, 1.1, 1.4, 1.1])

