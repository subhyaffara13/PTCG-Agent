
def test_lasso_selector(ax, kwargs):
    onselect = mock.Mock(spec=noop, return_value=None)

    tool = widgets.LassoSelector(ax, onselect=onselect, **kwargs)
    MouseEvent._from_ax_coords("button_press_event", ax, (100, 100), 1)._process()
    MouseEvent._from_ax_coords("motion_notify_event", ax, (125, 125), 1)._process()
    MouseEvent._from_ax_coords("button_release_event", ax, (150, 150), 1)._process()

    onselect.assert_called_once_with([(100, 100), (125, 125), (150, 150)])

