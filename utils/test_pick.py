
def test_pick():
    fig = plt.figure()
    fig.text(.5, .5, "hello", ha="center", va="center", picker=True)
    fig.canvas.draw()

    picks = []
    def handle_pick(event):
        assert event.mouseevent.key == "a"
        picks.append(event)
    fig.canvas.mpl_connect("pick_event", handle_pick)

    KeyEvent("key_press_event", fig.canvas, "a")._process()
    MouseEvent("button_press_event", fig.canvas,
               *fig.transFigure.transform((.5, .5)),
               MouseButton.LEFT)._process()
    KeyEvent("key_release_event", fig.canvas, "a")._process()
    assert len(picks) == 1

