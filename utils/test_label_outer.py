
def test_label_outer(remove_ticks, layout_engine, with_colorbar):
    fig = plt.figure(layout=layout_engine)
    axs = fig.subplots(2, 2, sharex=True, sharey=True)
    for ax in axs.flat:
        ax.set(xlabel="foo", ylabel="bar")
        if with_colorbar:
            fig.colorbar(mpl.cm.ScalarMappable(), ax=ax)
        ax.label_outer(remove_inner_ticks=remove_ticks)
    check_ticklabel_visible(
        axs.flat, [False, False, True, True], [True, False, True, False])
    if remove_ticks:
        check_tick1_visible(
            axs.flat, [False, False, True, True], [True, False, True, False])
    else:
        check_tick1_visible(
            axs.flat, [True, True, True, True], [True, True, True, True])

