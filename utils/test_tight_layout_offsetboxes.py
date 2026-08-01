
def test_tight_layout_offsetboxes():
    # 0.
    # - Create 4 subplots
    # - Plot a diagonal line on them
    # - Use tight_layout
    #
    # 1.
    # - Same 4 subplots
    # - Surround each plot with 7 boxes
    # - Use tight_layout
    # - See that the squares are included in the tight_layout and that the squares do
    #   not overlap
    #
    # 2.
    # - Make the squares around the Axes invisible
    # - See that the invisible squares do not affect the tight_layout
    rows = cols = 2
    colors = ['red', 'blue', 'green', 'yellow']
    x = y = [0, 1]

    def _subplots(with_boxes):
        fig, axs = plt.subplots(rows, cols)
        for ax, color in zip(axs.flat, colors):
            ax.plot(x, y, color=color)
            if with_boxes:
                add_offsetboxes(ax, 20, color=color)
        return fig, axs

    # 0.
    fig0, axs0 = _subplots(False)
    fig0.tight_layout()

    # 1.
    fig1, axs1 = _subplots(True)
    fig1.tight_layout()

    # The AnchoredOffsetbox should be added to the bounding of the Axes, causing them to
    # be smaller than the plain figure.
    for ax0, ax1 in zip(axs0.flat, axs1.flat):
        bbox0 = ax0.get_position()
        bbox1 = ax1.get_position()
        assert bbox1.x0 > bbox0.x0
        assert bbox1.x1 < bbox0.x1
        assert bbox1.y0 > bbox0.y0
        assert bbox1.y1 < bbox0.y1

    # No AnchoredOffsetbox should overlap with another.
    bboxes = []
    for ax1 in axs1.flat:
        for child in ax1.get_children():
            if not isinstance(child, AnchoredOffsetbox):
                continue
            bbox = child.get_window_extent()
            for other_bbox in bboxes:
                assert not bbox.overlaps(other_bbox)
            bboxes.append(bbox)

    # 2.
    fig2, axs2 = _subplots(True)
    for ax in axs2.flat:
        for child in ax.get_children():
            if isinstance(child, AnchoredOffsetbox):
                child.set_visible(False)
    fig2.tight_layout()
    # The invisible AnchoredOffsetbox should not count for tight layout, so it should
    # look the same as when they were never added.
    for ax0, ax2 in zip(axs0.flat, axs2.flat):
        bbox0 = ax0.get_position()
        bbox2 = ax2.get_position()
        assert_array_equal(bbox2.get_points(), bbox0.get_points())

