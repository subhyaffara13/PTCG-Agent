
def test_redraw_in_frame():
    fig, ax = plt.subplots(1, 1)
    ax.plot([1, 2, 3])
    fig.canvas.draw()
    ax.redraw_in_frame()

