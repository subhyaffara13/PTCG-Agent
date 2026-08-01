
def test_shared_with_aspect_3():
    # Different aspect ratios:
    for adjustable in ['box', 'datalim']:
        fig, axs = plt.subplots(nrows=2, sharey=True)
        axs[0].set_aspect(2, adjustable=adjustable)
        axs[1].set_aspect(0.5, adjustable=adjustable)
        axs[0].plot([1, 2], [3, 4])
        axs[1].plot([3, 4], [1, 2])
        plt.draw()  # Trigger apply_aspect().
        assert axs[0].get_xlim() != axs[1].get_xlim()
        assert axs[0].get_ylim() == axs[1].get_ylim()
        fig_aspect = fig.bbox_inches.height / fig.bbox_inches.width
        for ax in axs:
            p = ax.get_position()
            box_aspect = p.height / p.width
            lim_aspect = ax.viewLim.height / ax.viewLim.width
            expected = fig_aspect * box_aspect / lim_aspect
            assert round(expected, 4) == round(ax.get_aspect(), 4)

