
def test_radio_buttons_activecolor_change(fig_test, fig_ref):
    widgets.RadioButtons(fig_ref.subplots(), ['tea', 'coffee'],
                         activecolor='green')

    # Test property setter.
    cb = widgets.RadioButtons(fig_test.subplots(), ['tea', 'coffee'],
                              activecolor='red')
    cb.activecolor = 'green'

