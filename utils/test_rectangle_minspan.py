
def test_rectangle_minspan(ax, spancoords, minspanx, x1, minspany, y1):

    onselect = mock.Mock(spec=noop, return_value=None)

    x0, y0 = (10, 10)
    if spancoords == 'pixels':
        minspanx, minspany = (ax.transData.transform((x1, y1)) -
                              ax.transData.transform((x0, y0)))

    tool = widgets.RectangleSelector(ax, onselect=onselect, interactive=True,
                                     spancoords=spancoords,
                                     minspanx=minspanx, minspany=minspany)
    # Too small to create a selector
    click_and_drag(tool, start=(x0, x1), end=(y0, y1))
    assert not tool._selection_completed
    onselect.assert_not_called()

    click_and_drag(tool, start=(20, 20), end=(30, 30))
    assert tool._selection_completed
    onselect.assert_called_once()

    # Too small to create a selector. Should clear existing selector, and
    # trigger onselect because there was a preexisting selector
    onselect.reset_mock()
    click_and_drag(tool, start=(x0, y0), end=(x1, y1))
    assert not tool._selection_completed
    onselect.assert_called_once()
    (epress, erelease), kwargs = onselect.call_args
    assert epress.xdata == x0
    assert epress.ydata == y0
    assert erelease.xdata == x1
    assert erelease.ydata == y1
    assert kwargs == {}

