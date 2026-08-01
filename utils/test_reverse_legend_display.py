
def test_reverse_legend_display(fig_test, fig_ref):
    """Check that the rendered legend entries are reversed"""
    ax = fig_test.subplots()
    ax.plot([1], 'ro', label="first")
    ax.plot([2], 'bx', label="second")
    ax.legend(reverse=True)

    ax = fig_ref.subplots()
    ax.plot([2], 'bx', label="second")
    ax.plot([1], 'ro', label="first")
    ax.legend()

