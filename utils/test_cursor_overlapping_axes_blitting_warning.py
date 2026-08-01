
def test_cursor_overlapping_axes_blitting_warning():
    """Test that a warning is raised and useblit is disabled for overlapping axes."""
    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax2 = fig.add_axes([0.2, 0.2, 0.6, 0.6])  # Explicitly overlaps ax1

    match_text = (
        "Cursor blitting is currently not supported on "
        "overlapping axes"
    )
    with pytest.warns(UserWarning, match=match_text):
        cursor = widgets.Cursor(ax1, useblit=True)

    assert cursor.useblit is False

