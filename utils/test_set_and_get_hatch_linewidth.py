
def test_set_and_get_hatch_linewidth(fig_test, fig_ref):
    ax_test = fig_test.add_subplot()
    ax_ref = fig_ref.add_subplot()

    lw = 2.0

    with plt.rc_context({"hatch.linewidth": lw}):
        ax_ref.add_patch(mpatches.Rectangle((0, 0), 1, 1, hatch="x"))

    ax_test.add_patch(mpatches.Rectangle((0, 0), 1, 1, hatch="x"))
    ax_test.patches[0].set_hatch_linewidth(lw)

    assert ax_ref.patches[0].get_hatch_linewidth() == lw
    assert ax_test.patches[0].get_hatch_linewidth() == lw

