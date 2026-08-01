
def test_quiverkey_zorder(fig_test, fig_ref, zorder):
    draw_quiverkey_zorder_argument(fig_test, zorder=zorder)
    draw_quiverkey_setzorder(fig_ref, zorder=zorder)

