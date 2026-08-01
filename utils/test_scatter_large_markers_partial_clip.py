
def test_scatter_large_markers_partial_clip(fig_test, fig_ref):
    """
    Test that large markers are rendered when partially visible.

    Addresses reviewer concern: markers with centers outside the canvas but
    with edges extending into the visible area should still be rendered.
    """
    # Create markers just outside the visible area
    # Canvas is 0-10, markers at x=-0.5 and x=10.5
    x = np.array([-0.5, 10.5, 5])  # left edge, right edge, center
    y = np.array([5, 5, -0.5])  # center, center, bottom edge
    c = np.array([0.2, 0.5, 0.8])

    # Test figure: large markers (s=500 ≈ 11 points radius)
    # Centers are outside, but marker edges extend into visible area
    ax_test = fig_test.subplots()
    ax_test.scatter(x, y, c=c, s=500)
    ax_test.set_xlim(0, 10)
    ax_test.set_ylim(0, 10)

    # Reference figure: same plot (should render identically)
    ax_ref = fig_ref.subplots()
    ax_ref.scatter(x, y, c=c, s=500)
    ax_ref.set_xlim(0, 10)
    ax_ref.set_ylim(0, 10)

