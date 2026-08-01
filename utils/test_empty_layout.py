
def test_empty_layout():
    """Test that tight layout doesn't cause an error when there are no Axes."""
    fig = plt.gcf()
    fig.tight_layout()

