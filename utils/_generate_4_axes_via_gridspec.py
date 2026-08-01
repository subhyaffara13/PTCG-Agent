
def _generate_4_axes_via_gridspec():
    gs = mpl.gridspec.GridSpec(2, 2)
    ax_tl = plt.subplot(gs[0, 0])
    ax_ll = plt.subplot(gs[1, 0])
    ax_tr = plt.subplot(gs[0, 1])
    ax_lr = plt.subplot(gs[1, 1])

    return gs, [ax_tl, ax_ll, ax_tr, ax_lr]

