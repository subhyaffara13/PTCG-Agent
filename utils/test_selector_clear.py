
def test_selector_clear(ax, selector):
    kwargs = dict(ax=ax, interactive=True)
    if selector == 'span':
        Selector = widgets.SpanSelector
        kwargs['direction'] = 'horizontal'
        kwargs['onselect'] = noop
    else:
        Selector = widgets.RectangleSelector

    tool = Selector(**kwargs)
    click_and_drag(tool, start=(10, 10), end=(100, 120))

    # press-release event outside the selector to clear the selector
    click_and_drag(tool, start=(130, 130), end=(130, 130))
    assert not tool._selection_completed

    kwargs['ignore_event_outside'] = True
    tool = Selector(**kwargs)
    assert tool.ignore_event_outside
    click_and_drag(tool, start=(10, 10), end=(100, 120))

    # press-release event outside the selector ignored
    click_and_drag(tool, start=(130, 130), end=(130, 130))
    assert tool._selection_completed

    KeyEvent("key_press_event", ax.figure.canvas, "escape")._process()
    assert not tool._selection_completed

