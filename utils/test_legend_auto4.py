
def test_legend_auto4():
    """
    Check that the legend location with automatic placement is the same,
    whatever the histogram type is. Related to issue #9580.
    """
    # NB: barstacked is pointless with a single dataset.
    fig, axs = plt.subplots(ncols=3, figsize=(6.4, 2.4))
    leg_bboxes = []
    for ax, ht in zip(axs.flat, ('bar', 'step', 'stepfilled')):
        ax.set_title(ht)
        # A high bar on the left but an even higher one on the right.
        ax.hist([0] + 5*[9], bins=range(10), label="Legend", histtype=ht)
        leg = ax.legend(loc="best")
        fig.canvas.draw()
        leg_bboxes.append(
            leg.get_window_extent().transformed(ax.transAxes.inverted()))

    # The histogram type "bar" is assumed to be the correct reference.
    assert_allclose(leg_bboxes[1].bounds, leg_bboxes[0].bounds)
    assert_allclose(leg_bboxes[2].bounds, leg_bboxes[0].bounds)

