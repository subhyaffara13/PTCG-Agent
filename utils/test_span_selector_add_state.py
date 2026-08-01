
def test_span_selector_add_state(ax):
    tool = widgets.SpanSelector(ax, noop, 'horizontal',
                                interactive=True)

    with pytest.raises(ValueError):
        tool.add_state('unsupported_state')
    with pytest.raises(ValueError):
        tool.add_state('center')
    with pytest.raises(ValueError):
        tool.add_state('square')

    tool.add_state('move')

