
def test_empty_bar_chart_with_legend():
    """Test legend when bar chart is empty with a label."""
    # related to issue #13003. Calling plt.legend() should not
    # raise an IndexError.
    plt.bar([], [], label='test')
    plt.legend()

