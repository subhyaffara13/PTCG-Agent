
def test_scatter_c_facecolor_warning_integration(c, facecolor):
    """Test the warning through the actual scatter plot creation."""
    fig, ax = plt.subplots()
    x = [0, 1] if isinstance(c, (list, tuple)) else [0]
    y = x

    # Test with facecolors (plural)
    with pytest.warns(UserWarning, match=WARN_MSG):
        ax.scatter(x, y, c=c, facecolors=facecolor)

    # Test with facecolor (singular)
    with pytest.warns(UserWarning, match=WARN_MSG):
        ax.scatter(x, y, c=c, facecolor=facecolor)

