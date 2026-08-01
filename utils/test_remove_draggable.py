
def test_remove_draggable():
    fig, ax = plt.subplots()
    an = ax.annotate("foo", (.5, .5))
    an.draggable(True)
    an.remove()
    MouseEvent("button_release_event", fig.canvas, 1, 1)._process()

