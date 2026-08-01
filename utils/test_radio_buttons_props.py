
def test_radio_buttons_props(fig_test, fig_ref):
    label_props = {'color': ['red'], 'fontsize': [24]}
    radio_props = {'facecolor': 'green', 'edgecolor': 'blue', 'linewidth': 2}

    widgets.RadioButtons(fig_ref.subplots(), ['tea', 'coffee'],
                         label_props=label_props, radio_props=radio_props)

    cb = widgets.RadioButtons(fig_test.subplots(), ['tea', 'coffee'])
    cb.set_label_props(label_props)
    # Setting the label size automatically increases default marker size, so we
    # need to do that here as well.
    cb.set_radio_props({**radio_props, 's': (24 / 2)**2})

