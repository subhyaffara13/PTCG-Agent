
def test_check_button_props(fig_test, fig_ref):
    label_props = {'color': ['red'], 'fontsize': [24]}
    frame_props = {'facecolor': 'green', 'edgecolor': 'blue', 'linewidth': 2}
    check_props = {'facecolor': 'red', 'linewidth': 2}

    widgets.CheckButtons(fig_ref.subplots(), ['tea', 'coffee'], [True, True],
                         label_props=label_props, frame_props=frame_props,
                         check_props=check_props)

    cb = widgets.CheckButtons(fig_test.subplots(), ['tea', 'coffee'],
                              [True, True])
    cb.set_label_props(label_props)
    # Setting the label size automatically increases default marker size, so we
    # need to do that here as well.
    cb.set_frame_props({**frame_props, 's': (24 / 2)**2})
    # FIXME: Axes.scatter promotes facecolor to edgecolor on unfilled markers,
    # but Collection.update doesn't do that (it forgot the marker already).
    # This means we cannot pass facecolor to both setters directly.
    check_props['edgecolor'] = check_props.pop('facecolor')
    cb.set_check_props({**check_props, 's': (24 / 2)**2})

