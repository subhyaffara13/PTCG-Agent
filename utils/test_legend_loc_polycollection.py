
def test_legend_loc_polycollection():
    # Test that the legend is placed in the correct
    # position for 'best' for polycollection
    x = [3, 4, 5]
    y1 = [1, 1, 1]
    y2 = [5, 5, 5]
    leg_bboxes = []
    fig, axs = plt.subplots(ncols=2, figsize=(10, 5))
    for ax, loc in zip(axs.flat, ('best', 'lower left')):
        ax.fill_between(x, y1, y2, color='gray', alpha=0.5, label='Shaded Area')
        ax.set_xlim(0, 6)
        ax.set_ylim(-1, 5)
        leg = ax.legend(loc=loc)
        fig.canvas.draw()
        leg_bboxes.append(
            leg.get_window_extent().transformed(ax.transAxes.inverted()))
    assert_allclose(leg_bboxes[1].bounds, leg_bboxes[0].bounds)

