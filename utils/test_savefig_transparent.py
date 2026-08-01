
def test_savefig_transparent(fig_test, fig_ref):
    # create two transparent subfigures with corresponding transparent inset
    # axes. the entire background of the image should be transparent.
    gs1 = fig_test.add_gridspec(3, 3, left=0.05, wspace=0.05)
    f1 = fig_test.add_subfigure(gs1[:, :])
    f2 = f1.add_subfigure(gs1[0, 0])

    ax12 = f2.add_subplot(gs1[:, :])

    ax1 = f1.add_subplot(gs1[:-1, :])
    iax1 = ax1.inset_axes([.1, .2, .3, .4])
    iax2 = iax1.inset_axes([.1, .2, .3, .4])

    ax2 = fig_test.add_subplot(gs1[-1, :-1])
    ax3 = fig_test.add_subplot(gs1[-1, -1])

    for ax in [ax12, ax1, iax1, iax2, ax2, ax3]:
        ax.set(xticks=[], yticks=[])
        ax.spines[:].set_visible(False)

