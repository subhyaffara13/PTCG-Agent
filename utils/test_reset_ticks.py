
def test_reset_ticks(fig_test, fig_ref):
    for fig in [fig_ref, fig_test]:
        ax = fig.add_subplot()
        ax.grid(True)
        ax.tick_params(
            direction='in', length=10, width=5, color='C0', pad=12,
            labelsize=14, labelcolor='C1', labelrotation=45,
            grid_color='C2', grid_alpha=0.8, grid_linewidth=3,
            grid_linestyle='--')
        fig.draw_without_rendering()

    # After we've changed any setting on ticks, reset_ticks will mean
    # re-creating them from scratch. This *should* appear the same as not
    # resetting them.
    for ax in fig_test.axes:
        ax.xaxis.reset_ticks()
        ax.yaxis.reset_ticks()

