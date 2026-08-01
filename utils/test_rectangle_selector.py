
def test_rectangle_selector(ax, kwargs):
    onselect = mock.Mock(spec=noop, return_value=None)

    tool = widgets.RectangleSelector(ax, onselect=onselect, **kwargs)
    MouseEvent._from_ax_coords("button_press_event", ax, (100, 100), 1)._process()
    MouseEvent._from_ax_coords("motion_notify_event", ax, (199, 199), 1)._process()
    # purposely drag outside of axis for release
    MouseEvent._from_ax_coords("button_release_event", ax, (250, 250), 1)._process()

    if kwargs.get('drawtype', None) not in ['line', 'none']:
        assert_allclose(tool.geometry,
                        [[100., 100, 199, 199, 100],
                         [100, 199, 199, 100, 100]],
                        err_msg=tool.geometry)

    onselect.assert_called_once()
    (epress, erelease), kwargs = onselect.call_args
    assert epress.xdata == 100
    assert epress.ydata == 100
    assert erelease.xdata == 199
    assert erelease.ydata == 199
    assert kwargs == {}

