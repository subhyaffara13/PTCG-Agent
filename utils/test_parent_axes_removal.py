
def test_parent_axes_removal():

    fig, (ax_radio, ax_checks) = plt.subplots(1, 2)

    radio = widgets.RadioButtons(ax_radio, ['1', '2'], 0)
    checks = widgets.CheckButtons(ax_checks, ['1', '2'], [True, False])

    ax_checks.remove()
    ax_radio.remove()
    with io.BytesIO() as out:
        # verify that saving does not raise
        fig.savefig(out, format='raw')

    # verify that this method which is triggered by a draw_event callback when
    # blitting is enabled does not raise.  Calling private methods is simpler
    # than trying to force blitting to be enabled with Agg or use a GUI
    # framework.
    renderer = fig._get_renderer()
    evt = DrawEvent('draw_event', fig.canvas, renderer)
    radio._clear(evt)
    checks._clear(evt)

