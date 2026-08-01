
def test_canvas_reinit():
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

    called = False

    def crashing_callback(fig, stale):
        nonlocal called
        fig.canvas.draw_idle()
        called = True

    fig, ax = plt.subplots()
    fig.stale_callback = crashing_callback
    # this should not raise
    canvas = FigureCanvasQTAgg(fig)
    fig.stale = True
    assert called

