
def test_radio_button_active_conflict(ax):
    with pytest.warns(UserWarning,
                      match=r'Both the \*activecolor\* parameter'):
        rb = widgets.RadioButtons(ax, ['tea', 'coffee'], activecolor='red',
                                  radio_props={'facecolor': 'green'})
    # *radio_props*' facecolor wins over *activecolor*
    assert mcolors.same_color(rb._buttons.get_facecolor(), ['green', 'none'])

