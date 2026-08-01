
def test_masked_set_offsets(fig_ref, fig_test):
    x = np.ma.array([1, 2, 3, 4, 5], mask=[0, 0, 1, 1, 0])
    y = np.arange(1, 6)

    ax_test = fig_test.add_subplot()
    scat = ax_test.scatter(x, y)
    scat.set_offsets(np.ma.column_stack([x, y]))
    ax_test.set_xticks([])
    ax_test.set_yticks([])

    ax_ref = fig_ref.add_subplot()
    ax_ref.scatter([1, 2, 5], [1, 2, 5])
    ax_ref.set_xticks([])
    ax_ref.set_yticks([])

