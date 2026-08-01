
def test_mark_inset_unstales_viewlim(fig_test, fig_ref):
    inset, full = fig_test.subplots(1, 2)
    full.plot([0, 5], [0, 5])
    inset.set(xlim=(1, 2), ylim=(1, 2))
    # Check that mark_inset unstales full's viewLim before drawing the marks.
    mark_inset(full, inset, 1, 4)

    inset, full = fig_ref.subplots(1, 2)
    full.plot([0, 5], [0, 5])
    inset.set(xlim=(1, 2), ylim=(1, 2))
    mark_inset(full, inset, 1, 4)
    # Manually unstale the full's viewLim.
    fig_ref.canvas.draw()

