
def test_toolbar_home_restores_autoscale():
    fig, ax = plt.subplots()
    ax.plot(range(11), range(11))

    tb = NavigationToolbar2(fig.canvas)
    tb.zoom()

    # Switch to log.
    KeyEvent("key_press_event", fig.canvas, "k", 100, 100)._process()
    KeyEvent("key_press_event", fig.canvas, "l", 100, 100)._process()
    assert ax.get_xlim() == ax.get_ylim() == (1, 10)  # Autolimits excluding 0.
    # Switch back to linear.
    KeyEvent("key_press_event", fig.canvas, "k", 100, 100)._process()
    KeyEvent("key_press_event", fig.canvas, "l", 100, 100)._process()
    assert ax.get_xlim() == ax.get_ylim() == (0, 10)  # Autolimits.

    # Zoom in from (x, y) = (2, 2) to (5, 5).
    start, stop = ax.transData.transform([(2, 2), (5, 5)])
    MouseEvent("button_press_event", fig.canvas, *start, MouseButton.LEFT)._process()
    MouseEvent("button_release_event", fig.canvas, *stop, MouseButton.LEFT)._process()
    # Go back to home.
    KeyEvent("key_press_event", fig.canvas, "h")._process()

    assert ax.get_xlim() == ax.get_ylim() == (0, 10)
    # Switch to log.
    KeyEvent("key_press_event", fig.canvas, "k", 100, 100)._process()
    KeyEvent("key_press_event", fig.canvas, "l", 100, 100)._process()
    assert ax.get_xlim() == ax.get_ylim() == (1, 10)  # Autolimits excluding 0.

