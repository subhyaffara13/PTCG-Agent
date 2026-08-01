
def test_waitforbuttonpress(recwarn):  # recwarn undoes warn filters at exit.
    warnings.filterwarnings("ignore", "cannot show the figure")
    fig = plt.figure()
    assert fig.waitforbuttonpress(timeout=.1) is None
    Timer(.1, KeyEvent("key_press_event", fig.canvas, "z")._process).start()
    assert fig.waitforbuttonpress() is True
    Timer(.1, MouseEvent("button_press_event", fig.canvas, 0, 0, 1)._process).start()
    assert fig.waitforbuttonpress() is False

