
def test_grab_clear():
    fig, ax = plt.subplots()

    fig.canvas.grab_mouse(ax)
    assert fig.canvas.mouse_grabber == ax

    fig.clear()
    assert fig.canvas.mouse_grabber is None

