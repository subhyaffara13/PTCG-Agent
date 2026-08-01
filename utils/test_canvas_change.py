
def test_canvas_change():
    fig = plt.figure()
    # Replaces fig.canvas
    canvas = FigureCanvasBase(fig)
    # Should still work.
    plt.close(fig)
    assert not plt.fignum_exists(fig.number)

