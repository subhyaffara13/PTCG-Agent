
def test_legend_text():
    # Test that legend is place in the correct
    # position for 'best' when there is text in figure
    fig, axs = plt.subplots(ncols=2, figsize=(10, 5))
    leg_bboxes = []
    for ax, loc in zip(axs.flat, ('best', 'lower left')):
        x = [1, 2]
        y = [2, 1]
        ax.plot(x, y, label='plot name')
        ax.text(1.5, 2, 'some text blahblah', verticalalignment='top')
        leg = ax.legend(loc=loc)
        fig.canvas.draw()
        leg_bboxes.append(
            leg.get_window_extent().transformed(ax.transAxes.inverted()))
    assert_allclose(leg_bboxes[1].bounds, leg_bboxes[0].bounds)

