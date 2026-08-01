
def test__buttons_callbacks(ax, widget):
    """Tests what https://github.com/matplotlib/matplotlib/pull/31031 fixed"""
    on_clicked = mock.Mock(spec=noop, return_value=None)
    button = widget(ax, ["Test Button"])
    button.on_clicked(on_clicked)
    MouseEvent._from_ax_coords(
        "button_press_event",
        ax,
        ax.transData.inverted().transform(ax.transAxes.transform(
            # (x, y) of the 0th button defined at `_Buttons._init_layout`
            (0.15, 0.5),
        )),
        1,
    )._process()
    on_clicked.assert_called_once()

