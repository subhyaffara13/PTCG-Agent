
def test_twin_remove(fig_test, fig_ref):
    ax_test = fig_test.add_subplot()
    ax_twinx = ax_test.twinx()
    ax_twiny = ax_test.twiny()
    ax_twinx.remove()
    ax_twiny.remove()

    ax_ref = fig_ref.add_subplot()
    # Ideally we also undo tick changes when calling ``remove()``, but for now
    # manually set the ticks of the reference image to match the test image
    ax_ref.xaxis.tick_bottom()
    ax_ref.yaxis.tick_left()

