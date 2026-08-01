
def test_double_resize():
    # Check that resizing a figure twice keeps the same window size
    fig, ax = plt.subplots()
    fig.canvas.draw()
    window = fig.canvas.manager.window

    w, h = 3, 2
    fig.set_size_inches(w, h)
    assert fig.canvas.width() == w * matplotlib.rcParams['figure.dpi']
    assert fig.canvas.height() == h * matplotlib.rcParams['figure.dpi']

    old_width = window.width()
    old_height = window.height()

    fig.set_size_inches(w, h)
    assert window.width() == old_width
    assert window.height() == old_height

