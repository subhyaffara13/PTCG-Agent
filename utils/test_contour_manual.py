
def test_contour_manual():
    # Manually specifying contour lines/polygons to plot.
    from matplotlib.contour import ContourSet

    fig, ax = plt.subplots(figsize=(4, 4))
    cmap = 'viridis'

    # Segments only (no 'kind' codes).
    lines0 = [[[2, 0], [1, 2], [1, 3]]]  # Single line.
    lines1 = [[[3, 0], [3, 2]], [[3, 3], [3, 4]]]  # Two lines.
    filled01 = [[[0, 0], [0, 4], [1, 3], [1, 2], [2, 0]]]
    filled12 = [[[2, 0], [3, 0], [3, 2], [1, 3], [1, 2]],  # Two polygons.
                [[1, 4], [3, 4], [3, 3]]]
    ContourSet(ax, [0, 1, 2], [filled01, filled12], filled=True, cmap=cmap)
    ContourSet(ax, [1, 2], [lines0, lines1], linewidths=3, colors=['r', 'k'])

    # Segments and kind codes (1 = MOVETO, 2 = LINETO, 79 = CLOSEPOLY).
    segs = [[[4, 0], [7, 0], [7, 3], [4, 3], [4, 0],
             [5, 1], [5, 2], [6, 2], [6, 1], [5, 1]]]
    kinds = [[1, 2, 2, 2, 79, 1, 2, 2, 2, 79]]  # Polygon containing hole.
    ContourSet(ax, [2, 3], [segs], [kinds], filled=True, cmap=cmap)
    ContourSet(ax, [2], [segs], [kinds], colors='k', linewidths=3)

