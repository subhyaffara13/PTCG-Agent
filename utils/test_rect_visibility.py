
def test_rect_visibility(fig_test, fig_ref):
    # Check that requesting an invisible selector makes it invisible
    ax_test = fig_test.subplots()
    _ = fig_ref.subplots()

    tool = widgets.RectangleSelector(ax_test, props={'visible': False})
    tool.extents = (0.2, 0.8, 0.3, 0.7)

