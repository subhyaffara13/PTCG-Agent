
def test_polar_alignment():
    # Test changing the vertical/horizontal alignment of a polar graph.
    angles = np.arange(0, 360, 90)
    grid_values = [0, 0.2, 0.4, 0.6, 0.8, 1]

    fig = plt.figure()
    rect = [0.1, 0.1, 0.8, 0.8]

    horizontal = fig.add_axes(rect, polar=True, label='horizontal')
    horizontal.set_thetagrids(angles)

    vertical = fig.add_axes(rect, polar=True, label='vertical')
    vertical.patch.set_visible(False)

    for i in range(2):
        fig.axes[i].set_rgrids(
            grid_values, angle=angles[i],
            horizontalalignment='left', verticalalignment='top')

