
def test_RadioButtons(ax):
    radio = widgets.RadioButtons(ax, ('Radio 1', 'Radio 2', 'Radio 3'))
    radio.set_active(1)
    assert radio.value_selected == 'Radio 2'
    assert radio.index_selected == 1
    radio.clear()
    assert radio.value_selected == 'Radio 1'
    assert radio.index_selected == 0

