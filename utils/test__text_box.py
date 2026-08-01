
def test_TextBox(ax, toolbar):
    # Avoid "toolmanager is provisional" warning.
    plt.rcParams._set("toolbar", toolbar)

    submit_event = mock.Mock(spec=noop, return_value=None)
    text_change_event = mock.Mock(spec=noop, return_value=None)
    tool = widgets.TextBox(ax, '')
    tool.on_submit(submit_event)
    tool.on_text_change(text_change_event)

    assert tool.text == ''

    MouseEvent._from_ax_coords("button_press_event", ax, (.5, .5), 1)._process()

    tool.set_val('x**2')

    assert tool.text == 'x**2'
    assert text_change_event.call_count == 1

    tool.begin_typing()
    tool.stop_typing()

    assert submit_event.call_count == 2

    MouseEvent._from_ax_coords("button_press_event", ax, (.5, .5), 1)._process()
    KeyEvent("key_press_event", ax.figure.canvas, "+")._process()
    KeyEvent("key_press_event", ax.figure.canvas, "5")._process()

    assert text_change_event.call_count == 3

