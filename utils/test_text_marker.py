
def test_text_marker(fig_ref, fig_test):
    ax_ref = fig_ref.add_subplot()
    ax_test = fig_test.add_subplot()

    ax_ref.plot(0, 0, marker=r'o', markersize=100, markeredgewidth=0)
    ax_test.plot(0, 0, marker=r'$\bullet$', markersize=100, markeredgewidth=0)

