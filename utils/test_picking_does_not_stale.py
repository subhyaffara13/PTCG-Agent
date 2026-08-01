
def test_picking_does_not_stale():
    fig, ax = plt.subplots()
    ax.scatter([0], [0], [1000], picker=True)
    fig.canvas.draw()
    assert not fig.stale

    mouse_event = SimpleNamespace(x=ax.bbox.x0 + ax.bbox.width / 2,
                                  y=ax.bbox.y0 + ax.bbox.height / 2,
                                  inaxes=ax, guiEvent=None)
    fig.pick(mouse_event)
    assert not fig.stale

